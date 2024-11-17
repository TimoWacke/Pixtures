from fastapi import APIRouter, HTTPException, Path
import asyncio
from cachetools import TTLCache
import requests

from app.db.models.art_pieces_model import ArtPiecesModel, collection_name as art_pieces_collection
from app.db.base_collection import BaseCollection
from app.core.settings import settings


router = APIRouter()

# Cache with max size and expiration duration (e.g., 128 entries, 10 minutes)
mockup_cache = TTLCache(maxsize=128, ttl=600)  # TTL is in seconds


@router.get("/{art_piece_id}")
async def get_mockup_url(
    art_piece_id: str = Path(...)
) -> list[str]:
    """
    Fetch mockup URLs for the given art_piece_id, using a cached result if available.
    """
    try:
        # Return cached result
        if art_piece_id in mockup_cache:
            return mockup_cache[art_piece_id]

        # If not cached, start the task
        task = asyncio.create_task(generate_mockup_task(art_piece_id))
        result = await task
        mockup_cache[art_piece_id] = result  # Cache the result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_mockup_task(art_piece_id: str) -> list[str]:
    """
    Long-running task for generating mockup URLs.
    """
    # Use run_in_executor to offload blocking code
    return await asyncio.get_running_loop().run_in_executor(
        None, request_mockup_url, art_piece_id
    )


def request_mockup_url(art_piece_id: str) -> list[str]:
    """
    Blocking function for generating mockup URLs.
    """
    # Simulate a blocking operation here
    collection = BaseCollection(
        collection_name=art_pieces_collection,
        model_class=ArtPiecesModel
    )
    piece = collection.get_by_id(art_piece_id)

    xwidth = piece.width
    yheight = piece.height

    url_to_file = settings.SELF_DOMAIN + settings.API_V1_STR + "/artpiece/" + str(piece.id)

    mockreqs = ["Lifestyle 11", "Lifestyle 4", "Lifestyle 2"]
    mockup_url = []
    horizontal = xwidth > yheight
    ratio = 18 / 24
    border = 0.075 * min(xwidth, yheight)
    awidth = (yheight / ratio if horizontal else xwidth) + 2 * border
    aheight = (yheight if horizontal else xwidth / ratio) + 2 * border

    options = {
        "variant_ids": [7],
        "format": "jpg",
        "option_groups": mockreqs,
        "files": [
            {
                "placement": "default",
                "image_url": url_to_file,
                "position": {
                    "area_width": awidth,
                    "area_height": aheight,
                    "width": xwidth,
                    "height": yheight,
                    "left": (awidth - xwidth) / 2,
                    "top": (aheight - yheight) / 2
                }
            }
        ]
    }

    response = requests.post(
        'https://api.printful.com/mockup-generator/create-task/3',
        headers={"Authorization": f"Bearer {settings.PRINTFUL_BEARER}"},
        json=options
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to create mockup task")

    task_key = response.json().get('result', {}).get('task_key')
    if not task_key:
        raise HTTPException(status_code=400, detail="No task key returned")

    while len(mockup_url) < len(mockreqs):
        import time
        time.sleep(1)

        status_response = requests.get(
            f'https://api.printful.com/mockup-generator/task?task_key={task_key}',
            headers={"Authorization": f"Bearer {settings.PRINTFUL_BEARER}"}
        )

        if status_response.status_code != 200:
            raise HTTPException(status_code=status_response.status_code, detail="Failed to check task status")

        status_data = status_response.json().get('result', {})
        if status_data.get('status') == 'completed':
            mockup_url.append(status_data['mockups'][0]['mockup_url'])
            extra_mockups = status_data['mockups'][0].get('extra', [])
            for extra in extra_mockups:
                mockup_url.append(extra.get('url'))

    return mockup_url[::-1]
