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

    FRONTEND_DOMAIN: Optional[str] = None
    SELF_DOMAIN: str = "https://pixtures.sea.hamburg"

    PRINTFUL_BEARER: str

    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: str = "27017"
    MONGO_DATABASE: str = "pixtures"

    # Selenium WebDriver settings
    CHROME_BIN: str = "/usr/bin/chromium"
    CHROMEDRIVER_PATH: str = "/usr/bin/chromedriver"
    CHROME_FLAGS: str = "--headless --disable-gpu --no-sandbox --disable-dev-shm-usage"

    @property
    def MAP_URL(self) -> Optional[list[str]]:
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

    @property
    def FRONTEND_DOMAINS(self) -> list[str]:
        domains = [
            "https://loyalty.sea.hamburg",
            "https://sea.hamburg"
        ]
        if self.FRONTEND_DOMAIN:
            return [self.FRONTEND_DOMAIN] + domains
        return domains

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()
