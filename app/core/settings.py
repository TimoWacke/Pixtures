from pydantic_settings import BaseSettings
from enum import Enum
from typing import Optional


class EnvironmentType(str, Enum):
    LOCAL = 'local'
    DEV = 'dev'
    STAGING = 'staging'
    PROD = 'prod'


class Settings(BaseSettings):
    APP_PORT: str = "8000"
    HOST: str = "0.0.0.0"

    PROJECT_NAME: str = "PiXTURES"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: EnvironmentType = EnvironmentType.PROD

    FRONTEND_DOMAINS: Optional[list[str]] = [
        "https://loyalty.sea.hamburg",
        "https://sea.hamburg",
        "http://localhost:8080"
    ]
    SELF_DOMAIN: str = "https://pixtures.sea.hamburg"

    PRINTFUL_BEARER: str

    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: str = "27017"
    MONGO_DATABASE: str = "pixtures"

    SELENIUM_URL: str = "http://selenium-hub:4444/wd/hub"

    @property
    def MAP_URL(self) -> str:
        if self.ENVIRONMENT == EnvironmentType.LOCAL:
            return "https://pixtures.sea.hamburg/static/map.html"
        if self.ENVIRONMENT == EnvironmentType.PROD:
            return "http://pixtures:6969/static/map.html"

    @property
    def MONGO_URI(self) -> str:
        return (
            f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}?authSource=admin"
        )

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()
