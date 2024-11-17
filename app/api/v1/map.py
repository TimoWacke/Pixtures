from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from http import HTTPStatus
from io import BytesIO
import logging

from app.hooks.get_map_hook import GetMapHook


"""
Import is intentionally incorrect, since the API used for Scraping the maps is
created in the MapAPI.Dockerfile. This same Dockerfile flattens the folder
structure between:
- api/v1/get_map.py
- hooks/map_hook.py
- core/settings.py
to them being all in the same folder
"""

# Initialize Flask app
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the GetMapHook instance
get_map_hook = GetMapHook()


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    lng: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")

    @field_validator("lat", "lng", mode="before")
    def validate_required(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} is required.")
        return value


class MapCoordinates(Coordinates):
    zoom: int = Field(12, ge=0, le=20, description="Zoom level (0-20)")
    width: int = Field(800, ge=0, description="Image width in pixels")
    height: int = Field(600, ge=0, description="Image height in pixels")


@router.get('/screenshot')
def get_map_screenshot(
    coords: MapCoordinates = Query(...)
) -> StreamingResponse:
    """
    Endpoint to get a map screenshot for given coordinates.

    Query Parameters:
        lat (float): Latitude of the location
        lng (float): Longitude of the location
        zoom (int, optional): Zoom level (0-20). Defaults to 12
        width (int, optional): Image width in pixels. Defaults to 800
        height (int, optional): Image height in pixels. Defaults to 600

    Returns:
        Image file or JSON error response
    """
    try:
        # Get the screenshot using GetMapHook
        image, location_name = get_map_hook.screenshot(
            lat=coords.lat,
            lng=coords.lng,
            zm=coords.zoom,
            w=coords.width,
            h=coords.height
        )

        # Convert PIL Image to bytes
        img_byte_array = BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        # Cre # Create a streaming response for the image
        response = StreamingResponse(
            img_byte_array, media_type="image/png"
        )

        # Add custom headers with metadata
        response.headers["X-Location-Name"] = location_name
        response.headers["X-Coordinates"] = f"{coords.lat},{coords.lng}"
        response.headers["X-Image-Size"] = f"{coords.width}x{coords.height}"

        return response

    except Exception as e:
        logger.error(f"Error generating screenshot: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to generate map screenshot",
                "details": str(e),
            },
        )


class LocationResponse(BaseModel):
    location: str
    coordinates: Coordinates


@router.get('/location')
def get_location_info(
    coords: Coordinates = Query(...)
) -> LocationResponse:
    """
    Endpoint to get location information without screenshot.

    Query Parameters:
        lat (float): Latitude of the location
        lng (float): Longitude of the location

    Returns:
        JSON response with location information
    """
    try:
        location_name = get_map_hook.get_location_name(coords.lat, coords.lng)
        return LocationResponse(
            location=location_name,
            coordinates=coords
        )

    except Exception as e:
        logger.error(f"Error retrieving location: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to retrieve location information",
                "details": str(e),
            },
        )
