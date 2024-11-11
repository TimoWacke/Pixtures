from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone


class BaseMongoModel(BaseModel):

    id: Optional[ObjectId] = Field(None, alias='_id')

    updated_at: Optional[datetime] = Field(None, alias='updatedAt')
    created_at: Optional[datetime] = Field(None, alias='createdAt')

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

    def to_mongo_dict(self):
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        return self.model_dump(by_alias=True, exclude_unset=True)
