from pydantic import BaseModel, Field, field_validator
import reverse_geocoder as rg
import logging


logger = logging.getLogger(__name__)


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    lng: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")

    @field_validator("lat", "lng", mode="before")
    def validate_required(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} is required.")
        return value

    class Config:
        extra = "allow"


class MapCoordinates(Coordinates):
    zoom: int = Field(12, ge=0, le=20, description="Zoom level (0-20)")
    width: int = Field(800, ge=0, description="Image width in pixels")
    height: int = Field(600, ge=0, description="Image height in pixels")


class Favorite(Coordinates):
    name: str
    zm: float

    # example data
    class Config:
        schema_extra = {
            "example": {
                "name": "Amsterdam",
                "lat": 52.365,
                "lng": 4.88,
                "zm": 14.9
            }
        }


class LocationAddress(BaseModel):
    lat: float
    lng: float = Field(..., alias='lon')
    name: str
    admin1: str
    admin2: str
    cc: str


class RegionService:
    def __init__(self):
        pass

    def get_location(self, coordinates: Coordinates) -> LocationAddress:
        location = rg.search((coordinates.lat, coordinates.lng))
        return LocationAddress(**location[0])

    def get_location_name(self, coordinates: Coordinates) -> str:
        location = self.get_location(coordinates)
        try:
            if location.name in location.admin1:
                return location.name
            if location.admin2:
                if location.name in location.admin2:
                    return location.name
            # If the location name is of many words separated by spaces
            # get a list of all workds with at least 4 characters
            words = [word for word in location.name.split() if len(word) >= 4]
            if words:
                if any(word in location.admin1 for word in words):
                    return location.name
                if location.admin2:
                    if any(word in location.admin2 for word in words):
                        return location.name
            if location.cc == "US":
                return location.name
            return location.admin1

        except Exception as e:
            logging.error(f"Error retrieving location: {e}")
            return location.name

    def get_suggested(self) -> list[Favorite]:

        json_data = [
            {"name": "Amsterdam", "lat": 52.365, "lng": 4.88, "zm": 14.9},
            {"name": "London", "lat": 51.5, "lng": -0.09, "zm": 13.8},
            {"name": "Paris", "lat": 48.8566, "lng": 2.33, "zm": 14.8},
            {"name": "Stockholm", "lat": 59.335, "lng": 18.0686, "zm": 14.3},
            {"name": "Cape Town", "lat": -34, "lng": 18.48, "zm": 14},
            {"name": "Rio d Janeiro", "lat": -22.93, "lng": -43.2, "zm": 14.4},
            {"name": "Tokyo", "lat": 35.7, "lng": 139.8, "zm": 12},
            {"name": "Bejing", "lat": 39.9, "lng": 116.4, "zm": 13},
            {"name": "Shanghai", "lat": 31.1, "lng": 121.55, "zm": 11.75},
            {"name": "Guangzhou", "lat": 22.8, "lng": 113.3, "zm": 11.4},
            {"name": "Hong Kong", "lat": 22.31, "lng": 114.17, "zm": 14.9},
            {"name": "New York", "lat": 40.733, "lng": -73.99, "zm": 14.6},
            {"name": "Los Angeles", "lat": 33.93, "lng": -118.2, "zm": 12.3},
            {"name": "Chicago", "lat": 41.8781, "lng": -87.67, "zm": 14.6}
        ]

        return [Favorite(**data) for data in json_data]
