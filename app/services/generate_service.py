from fastapi import UploadFile
from PIL import Image
from io import BytesIO
from bson import ObjectId
import base64

from pydantic import BaseModel, Field
from functools import lru_cache

from app.db.models.user_image_model import UserImageModel, collection_name as user_collection
from app.db.models.art_pieces_model import ArtPiecesModel
from app.db.base_collection import BaseCollection
from app.algorithms.map_face import MapFace
from app.hooks.get_map_hook import GetMapHook


class GenerateRequest(BaseModel):
    image_id: str = Field(alias='imageId')
    user_id: str = Field(alias='userId')
    latitude: float = Field(alias='lat')
    longitude: float = Field(alias='lng')
    zoom: float = Field(alias='zm')
    map_with: float = Field(alias='width')
    map_height: float = Field(alias='height')


class GenerateService:
    def __init__(self, user_id: ObjectId):
        self.user_id = user_id
        self.portraits = {}

        self.collection = BaseCollection(
            collection_name=user_collection,
            model_class=UserImageModel
        )

        self.art_collection = BaseCollection(
            collection_name='art_pieces',
            model_class=ArtPiecesModel
        )

    def submit_portrait(self, image_file: UploadFile) -> UserImageModel:

        image = Image.open(BytesIO(image_file.file.read()))
        file_extension = image_file.filename.split(".")[-1]

        buffered = BytesIO()
        image.save(buffered, format=file_extension)
        image_bytes = buffered.getvalue()

        width, height = image.size

        user_image = UserImageModel(
            user_id=self.user_id,
            image_content=base64.b64encode(image_bytes),
            file_extension=file_extension,
            width=width,
            height=height
        )

        created = self.collection.create(user_image)

        self.portraits[str(created.id)] = created

        return created

    def make_map_art(self, request: GenerateRequest) -> ArtPiecesModel:

        map_image, region_name = GetMapHook().screenshot(
            lat=request.latitude,
            lng=request.longitude,
            zm=request.zoom,
            w=request.map_with,
            h=request.map_height
        )

        image_id = ObjectId(request.image_id)
        assert self.user_id == ObjectId(request.user_id)

        if not str(image_id) in self.portraits:
            user_image = self.collection.get_by_id(image_id)
        else:
            user_image = self.portraits[str(image_id)]

        if not user_image:
            user_image = self.collection.get_by_id(image_id)

        pillow_portrait = Image.open(BytesIO(base64.b64decode(user_image.image_content)))

        map_face_algo = MapFace()

        result_im = map_face_algo.run(
            im=map_image,
            pt=pillow_portrait
        )

        result_width, result_height = result_im.size

        buffered = BytesIO()
        result_im.save(buffered, format='PNG')
        image_bytes = buffered.getvalue()

        art_piece = ArtPiecesModel(
            user_id=self.user_id,
            image_id=ObjectId(request.image_id),
            latitude=request.latitude,
            longitude=request.longitude,
            zoom=request.zoom,
            width=result_width,
            height=result_height,
            region=region_name,
            art_image=base64.b64encode(image_bytes)
        )

        created_art_piece = self.art_collection.create(art_piece)

        return created_art_piece


@lru_cache(maxsize=128)
def get_generate_service(userId: str) -> GenerateService:
    return GenerateService(ObjectId(userId))
