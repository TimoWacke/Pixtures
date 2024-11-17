import asyncio
from functools import lru_cache
from fastapi import APIRouter, HTTPException, Path
import requests
import logging
from app.core.settings import settings  # Assuming the bearer token is stored in settings
from app.db.base_collection import BaseCollection
from app.db.models.art_pieces_model import ArtPiecesModel, collection_name as art_pieces_collection


router = APIRouter()
logger = logging.getLogger(__name__)


async def sleep(ms: int):
    """Helper function for delaying (using asyncio.sleep to avoid blocking the event loop)."""
    await asyncio.sleep(ms / 1000)  # Convert milliseconds to seconds


@router.get("/{art_piece_id}")
async def get_mockup_url(
    art_piece_id: str = Path(...),
) -> list[str]:
    try:
        return request_mockup_url(art_piece_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@lru_cache(maxsize=128)
async def request_mockup_url(art_piece_id: str) -> list[str]:
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

    # Prepare the request to create a mockup

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
    logger.info(f"Creating mockup with options: {options}")

    # Send the request to Printful API
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

    # Poll for the mockup result
    while len(mockup_url) < len(mockreqs):
        await sleep(1000)  # Wait 1 second before polling again

        # Get the status of the task
        status_response = requests.get(
            f'https://api.printful.com/mockup-generator/task?task_key={task_key}',
            headers={"Authorization": f"Bearer {settings.PRINTFUL_BEARER}"}
        )

        if status_response.status_code != 200:
            raise HTTPException(status_code=status_response.status_code, detail="Failed to check task status")

        status_data = status_response.json().get('result', {})
        if status_data.get('status') == 'completed':
            mockup_url.append(status_data['mockups'][0]['mockup_url'])
            # Add extra mockups if available
            extra_mockups = status_data['mockups'][0].get('extra', [])
            for extra in extra_mockups:
                mockup_url.append(extra.get('url'))

    return mockup_url[::-1]  # Reverse the list to match the desired order
