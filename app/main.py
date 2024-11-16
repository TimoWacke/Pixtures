from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from app.core.startup_message import create_startup_message
from app.core.settings import settings
from app.core.router_register import RouterRegistry


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger = logging.getLogger("FastAPI")

    try:
        logger.info("Starting application")

        # if settings.ENVIRONMENT != "prod":
        create_startup_message()

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise e

    yield  # Application runs here

    # Shutdown
    try:
        logger.info("Shutting down application")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        raise e


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan,
        # docs_url=None if settings.ENVIRONMENT != "local" else "/docs",
        # redcos_url=None if settings.ENVIRONMENT != "local" else "/redoc",
    )

    if settings.FRONTEND_DOMAIN:
        try:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=settings.FRONTEND_DOMAINS,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        except Exception as e:
            logging.error(f"Error adding CORS middleware: {e}")
            raise e

    # Register routers
    try:
        registry = RouterRegistry(app)
        registry.setup()
        logging.info("Route registration complete")

    except Exception as e:
        logging.error(f"Error registering routes: {e}")
        raise e

    # Serve static files
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")

    return app


app = create_app()
