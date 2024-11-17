from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from app.core.settings import settings
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class MongoDBConnection:
    _instance = None
    _client = None

    # Singleton pattern using __new__
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls, *args, **kwargs)
            cls._instance.connect()  # Initialize only once
        return cls._instance

    def connect(self):
        if self._client is not None:  # Avoid reconnecting if already connected
            return
        try:
            connection_string = settings.MONGO_URI

            # Validate connection string
            if not connection_string.startswith('mongodb://'):
                raise ValueError('Invalid connection string')

            # Parse connection string
            parsed_uri = urlparse(connection_string)
            if 'authSource' not in parsed_uri.query and 'admin' not in connection_string:
                # Append authSource if not present
                separator = '&' if '?' in connection_string else '?'
                connection_string = f'{connection_string}{separator}authSource=admin'

            # initialize client
            self._client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000
            )

            # Verify connection
            self._client.admin.command('ping')
            logger.info('Connected to MongoDB')

        except ConnectionFailure as e:
            logger.error(f'Failed to connect to MongoDB: {e}')
            raise e

        except OperationFailure as e:
            logger.error(f'Authentication failed: {e}')
            raise e

        except Exception as e:
            logger.error(f'Unexpected error while connecting to MongoDB: {e}')
            raise e

    def get_client(self):
        if self._client is None:
            logger.error('MongoDB client is not initialized. Please check the connection.')
            raise ValueError("MongoDB client is not initialized.")
        return self._client

    def get_database(self, db_name):
        if self._client is None:
            logger.error('MongoDB client is not initialized. Cannot access database.')
            raise ValueError("MongoDB client is not initialized.")
        try:
            return self._client[db_name]
        except Exception as e:
            logger.error(f'Error accessing database {db_name}: {e}')
            raise

    def close(self):
        if self._client:
            self._client.close()
            logger.info('Connection to MongoDB closed')
            self._client = None
