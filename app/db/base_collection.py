from datetime import datetime, timezone
from typing import Generic, TypeVar, Optional, List, Type, Tuple, Any
from pydantic import BaseModel
from bson import ObjectId
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
import logging
from functools import wraps
import traceback

from app.db.connect import MongoDBConnection
from app.db.base_model import BaseMongoModel
from app.core.settings import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def handle_mongo_errors(func):
    """Decorator to handle MongoDB operation errors"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PyMongoError as e:
            logger.error(f"MongoDB error in {func.__name__}: {str(e)}")
            logger.debug(f"Stack trace: {traceback.format_exc()}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.debug(f"Stack trace: {traceback.format_exc()}")
            raise

    return wrapper


class BaseResponse(BaseModel):
    """Base response model with common fields"""

    id: str = None
    _id: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}


class BaseCollection(Generic[T]):
    """Base repository class for MongoDB operations"""

    def __init__(self, collection_name: str, model_class: Type[T]):
        self.database: Database = MongoDBConnection().get_database(settings.MONGO_DATABASE)
        self.collection: Collection = self.database[collection_name]
        self.model_class = model_class
        self.logger = logging.getLogger(f"{__name__}.{collection_name}")

        # Create indexes if needed
        self._setup_indexes()

    def _setup_indexes(self):
        """Setup any necessary indexes for the collection"""
        try:
            # Example: Create an index on created_at field
            self.collection.create_index("createdAt")
            # Add more indexes as needed
        except PyMongoError as e:
            self.logger.warning(f"Failed to create indexes: {str(e)}")

    @handle_mongo_errors
    def create(self, model: T) -> T:
        """Create a new document"""
        self.logger.info(f"Creating new {self.model_class.__name__} document")

        if isinstance(model, BaseMongoModel):
            model.created_at = datetime.now(timezone.utc)
            model.updated_at = model.created_at

        mongo_dict = model.to_mongo_dict() if hasattr(model, "to_mongo_dict") else model.model_dump(by_alias=True)

        result = self.collection.insert_one(mongo_dict)
        model.id = result.inserted_id

        self.logger.debug(f"Created document with ID: {result.inserted_id}")
        return model

    @handle_mongo_errors
    def get_by_id(self, id: ObjectId) -> Optional[T]:
        """Get a document by ID"""
        self.logger.debug(f"Fetching document by ID: {id}")

        if not isinstance(id, ObjectId):
            try:
                object_id = ObjectId(id)
            except Exception as e:
                self.logger.warning(f"Invalid ObjectId format: {id}", e)
                return None
        else:
            object_id = id

        document = self.collection.find_one({"_id": object_id})
        if document:
            return self.model_class(**document)
        return None

    @handle_mongo_errors
    def get_by_field(self, field: str, value: Any) -> Optional[T]:
        """Get a document by any field"""
        self.logger.debug(f"Fetching document by field: {field}={value}")

        document = self.collection.find_one({field: value})
        if document:
            return self.model_class(**document)
        return None

    @handle_mongo_errors
    def update(self, id: str, update_dict: dict) -> bool:
        """Update a document"""
        self.logger.info(f"Updating document {id}")
        self.logger.debug(f"Update data: {update_dict}")

        if not isinstance(id, ObjectId):
            try:
                object_id = ObjectId(id)
            except Exception as e:
                self.logger.warning(f"Invalid ObjectId format: {id}", e)
                return None
        else:
            object_id = id

        update_dict["updatedAt"] = datetime.now(timezone.utc)
        result = self.collection.update_one({"_id": object_id}, {"$set": update_dict})

        success = result.modified_count > 0
        if success:
            self.logger.debug(f"Successfully updated document {id}")
        else:
            self.logger.warning(f"Document {id} was not updated")
        return success

    @handle_mongo_errors
    def update_by_field(self, field: str, value: Any, update_dict: dict) -> bool:
        """Update a document by any field"""
        self.logger.info(f"Updating document by field: {field}={value}")
        self.logger.debug(f"Update data: {update_dict}")

        update_dict["updatedAt"] = datetime.now(timezone.utc)
        result = self.collection.update_one({field: value}, {"$set": update_dict})

        success = result.modified_count > 0
        if success:
            self.logger.debug(f"Successfully updated document with {field}={value}")
        else:
            self.logger.warning(f"Document with {field}={value} was not updated")
        return success

    @handle_mongo_errors
    def delete(self, id: str) -> bool:
        """Delete a document"""
        self.logger.info(f"Deleting document {id}")

        if not isinstance(id, ObjectId):
            try:
                object_id = ObjectId(id)
            except Exception as e:
                self.logger.warning(f"Invalid ObjectId format: {id}", e)
                return None
        else:
            object_id = id

        result = self.collection.delete_one({"_id": object_id})

        success = result.deleted_count > 0
        if success:
            self.logger.debug(f"Successfully deleted document {id}")
        else:
            self.logger.warning(f"Document {id} was not found or not deleted")
        return success

    @handle_mongo_errors
    def list(
        self, filter_dict: dict = None, skip: int = 0, limit: int = 50, sort_field: str = None, sort_order: int = 1
    ) -> Tuple[List[T], int]:
        """List documents with pagination"""
        self.logger.info("Listing documents")
        self.logger.debug(f"Filter: {filter_dict}, Skip: {skip}, Limit: {limit}, Sort: {sort_field}")

        query = filter_dict or {}

        # Get total count
        total = self.collection.count_documents(query)

        # Build cursor
        cursor = self.collection.find(query).skip(skip).limit(limit)
        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)

        # Get results and convert to models
        documents = [self.model_class(**doc) for doc in cursor]

        self.logger.info(f"Found {len(documents)} documents (total: {total})")
        return documents, total

    @handle_mongo_errors
    def bulk_create(self, models: List[T]) -> List[T]:
        """Create multiple documents"""
        self.logger.info(f"Bulk creating {len(models)} documents")

        current_time = datetime.now(timezone.utc)
        documents = []

        for model in models:
            if isinstance(model, BaseMongoModel):
                model.created_at = current_time
                model.updated_at = current_time

            mongo_dict = model.to_mongo_dict() if hasattr(model, "to_mongo_dict") else model.model_dump(by_alias=True)
            documents.append(mongo_dict)

        result = self.collection.insert_many(documents)

        # Update models with their new IDs
        for model, inserted_id in zip(models, result.inserted_ids):
            model.id = inserted_id

        self.logger.debug(f"Successfully created {len(models)} documents")
        return models

    @handle_mongo_errors
    def bulk_update(self, updates: List[Tuple[str, dict]]) -> int:
        """Bulk update documents

        Args:
            updates: List of tuples containing (id, update_dict)

        Returns:
            Number of documents updated
        """
        self.logger.info(f"Bulk updating {len(updates)} documents")

        current_time = datetime.now(timezone.utc)
        operations = []

        for doc_id, update_dict in updates:
            try:
                object_id = ObjectId(doc_id)
                update_dict["updatedAt"] = current_time
                operations.append({"update_one": {"filter": {"_id": object_id}, "update": {"$set": update_dict}}})
            except Exception as e:
                self.logger.warning(f"Invalid ObjectId format: {doc_id}", e)
                continue

        if not operations:
            return 0

        result = self.collection.bulk_write(operations)
        self.logger.debug(f"Successfully updated {result.modified_count} documents")
        return result.modified_count
