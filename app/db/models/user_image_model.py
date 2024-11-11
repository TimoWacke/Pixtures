
from app.db.base_model import BaseMongoModel
from typing import Optional
from bson import ObjectId


class UserImageModel(BaseMongoModel):
    user_id: Optional[ObjectId] = None
    image_content: Optional[bytes] = None
    file_extension: str
    width: int
    height: int


collection_name = 'user_images'
