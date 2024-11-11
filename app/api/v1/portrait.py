from fastapi import APIRouter, Form, File, UploadFile
from app.services.generate_service import get_generate_service
import logging
from bson import ObjectId


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/"
)
async def pre_save_portrait(
    userId: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Pre-save a portrait image for a user.
    """
    try:
        user_id = ObjectId(userId)
        service = get_generate_service(user_id)
        saved = service.submit_portrait(file)
        saved
        saved.image_content = None
        return saved
    except Exception as e:
        logger.error(f"Error saving portrait: {e}")
        raise e
