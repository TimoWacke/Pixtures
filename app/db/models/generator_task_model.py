
from app.db.base_model import BaseMongoModel
from typing import Optional
from bson import ObjectId


# TODO: refactor algortihms to use such a model


class GeneratorTaskModel(BaseMongoModel):
    image_id: ObjectId
    latitude: float
    longitude: float
    zoom: float
    width_of_map: int
    height_of_map: int
    preview_url: Optional[str] = None


collection_name = 'generator_tasks'
