from fastapi import APIRouter, Path
from fastapi.responses import Response
from bson import ObjectId
from app.core.settings import settings
import base64
from app.db.base_collection import BaseCollection
from app.db.models.art_pieces_model import (
    ArtPiecesModel,
    collection_name as art_pieces_collection
)

router = APIRouter()


@router.get("/{pieceId}")
async def generate_map(
    pieceId: str = Path(...),
):

    piece_id = ObjectId(pieceId)

    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )

    art_piece: ArtPiecesModel = collection.get_by_id(piece_id)

    # send file to user
    image_base64_encoded = art_piece.art_image
    image_extension = art_piece.file_extension

    return Response(
        content=base64.b64decode(image_base64_encoded),
        media_type=f"image/{image_extension}")


@router.get("/")
async def list_art_pieces():
    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )

    art_pieces = collection.list()
    # return all preview urls
    return [f"{settings.SELF_DOMAIN}/api/v1/artpiece/{str(art_piece._id)}" for art_piece in art_pieces]
