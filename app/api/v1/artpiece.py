from fastapi import APIRouter, Path
from fastapi.responses import Response
from bson import ObjectId
import pandas as pd
from functools import lru_cache
from app.core.settings import settings
import base64
from app.db.base_collection import BaseCollection
from app.db.models.art_pieces_model import (
    ArtPiecesModel,
    collection_name as art_pieces_collection
)


router = APIRouter()


@router.get("/id/{pieceId}")
async def generate_map(
    pieceId: str = Path(...),
):

    art_piece = get_artpiece_by_id_cached(pieceId)

    # send file to user
    image_base64_encoded = art_piece.art_image
    image_extension = art_piece.file_extension

    return Response(
        content=base64.b64decode(image_base64_encoded),
        media_type=f"image/{image_extension}")


@lru_cache(maxsize=128)
def get_artpiece_by_id_cached(pieceId: str) -> ArtPiecesModel:
    piece_id = ObjectId(pieceId)

    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )

    return collection.get_by_id(piece_id)


@router.get("/highlights")
def list_liked_pieces():
    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )

    art_pieces = collection.list()

    art_pieces = shuffle_controlled(art_pieces)

    # return all preview urls
    return [f"{settings.SELF_DOMAIN}/api/v1/artpiece/id/{str(art_piece.id)}" for art_piece in art_pieces]


@router.delete("/{pieceId}")
async def delete_art_piece(
    pieceId: str = Path(...),
):
    piece_id = ObjectId(pieceId)

    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )

    collection.delete(piece_id)

    return {"message": "Art piece deleted."}


@router.get("/like/{pieceId}")
async def like_art_piece(
    pieceId: str = Path(...),
):
    piece_id = ObjectId(pieceId)

    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )

    art_piece = collection.get_by_id(piece_id)

    art_piece.likes += 1

    update_dict = {
        "likes": art_piece.likes
    }

    collection.update(art_piece.id, update_dict)

    return {"message": "Art piece liked."}


def shuffle_controlled(artpieces: list[ArtPiecesModel], row_break=3) -> list[ArtPiecesModel]:
    """
        Shuffle the items in a controlled manner with a pattern of H and V,
        alternating based on a row break parameter.
        Where H is an item with a width greater than its height and V is the opposite.

        The pattern would look like:

        H V V
        V H V
        V V H
        H V V
        ...

        Args:
            items (list): List of objects with .width, .height and .likes properties.
            row_break (int): Number of rows before switching the horizontal count.

        Returns:
            list: Shuffled list of items in the specified pattern.
        """
    # Convert the list of items to a pandas DataFrame
    df = pd.DataFrame([(artpiece, artpiece.width, artpiece.height, artpiece.likes)
                      for artpiece in artpieces], columns=['item', 'width', 'height', 'likes'])

    # Determine the aspect ratio (horizontal or vertical)
    df['aspect'] = df['width'] > df['height']

    # Define a helper function to shuffle with prioritization by likes
    def weighted_shuffle(df):
        # Normalize likes to probabilities
        total_likes = df['likes'].sum()
        if total_likes == 0:
            return df.sample(frac=1, random_state=42)  # Equal weights if no likes
        weights = df['likes'] / total_likes
        return df.sample(frac=1, weights=weights, random_state=None)

    # Separate horizontal and vertical items, applying weighted shuffling
    horizontals = weighted_shuffle(df[df['aspect']])
    verticals = weighted_shuffle(df[~df['aspect']])

    # Prepare the shuffled list
    shuffled_list = []
    h_idx, v_idx = 0, 0

    def add_horizontal():
        nonlocal h_idx
        if h_idx < len(horizontals):
            shuffled_list.append(horizontals.iloc[h_idx]['item'])
            h_idx += 1

    def add_vertical():
        nonlocal v_idx
        if v_idx < len(verticals):
            shuffled_list.append(verticals.iloc[v_idx]['item'])
            v_idx += 1

    # Build the list with the pattern 1 horizontal, 3 vertical
    while h_idx < len(horizontals) or v_idx < len(verticals):
        # Add 1 horizontal if available
        add_horizontal()
        if h_idx % row_break == 0:
            add_horizontal()  # Add another horizontal if it's time to switch
        for _ in range(row_break):
            add_vertical()

    # The final shuffled list
    return shuffled_list
