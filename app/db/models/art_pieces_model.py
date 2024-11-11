
from app.db.base_model import BaseMongoModel
from typing import Optional
from bson import ObjectId


class ArtPiecesModel(BaseMongoModel):
    user_id: Optional[ObjectId] = None
    image_id: ObjectId
    latitude: float
    longitude: float
    zoom: float
    width: int
    height: int
    art_image: bytes
    region: str
    file_extension: str = 'PNG'


collection_name = 'art_pieces'
