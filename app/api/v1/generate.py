from fastapi import APIRouter
from concurrent.futures import ThreadPoolExecutor
import asyncio

from app.services.generate_service import get_generate_service, GenerateRequest
from app.core.settings import settings

import logging

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=1)  # Pool for Selenium tasks
logger = logging.getLogger(__name__)


@router.post("/")
async def generate_map(
    request: GenerateRequest
):
    """
    Generate a map image.
    """
    try:

        generator = get_generate_service(request.user_id)

        loop = asyncio.get_event_loop()
        art_piece = await loop.run_in_executor(executor, generator.make_map_art, request)

        return {
            "preview": f"{settings.SELF_DOMAIN}{settings.API_V1_STR}/artpiece/{str(art_piece.id)}",
            "id": str(art_piece.id),
            "location": art_piece.region
        }
    except Exception as e:
        logger.error(f"Error generating map: {e}")
        raise e
