# app/core/router_registry.py
from fastapi import APIRouter, FastAPI
from typing import List, Optional
import importlib
import pkgutil
import inspect
from pathlib import Path
import sys
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)


class RouterRegistry:
    """Automatically discovers and registers FastAPI routers from the API controllers directory."""

    def __init__(self, app: FastAPI, base_package: str = "app.api.v1"):
        self.app = app
        self.base_package = base_package
        self._discovered_routers: List[tuple[str, APIRouter]] = []

    def _get_package_path(self, package_name: str) -> Optional[Path]:
        """
        Safely get the package path using multiple methods.
        """
        try:
            # Try importing the package
            package = importlib.import_module(package_name)

            # Method 1: Try getting path from __file__
            if hasattr(package, '__file__') and package.__file__:
                return Path(package.__file__).parent

            # Method 2: Try getting path from __path__
            if hasattr(package, '__path__') and package.__path__:
                return Path(package.__path__[0])

            # Method 3: Try finding package in sys.modules
            for path in sys.path:
                potential_path = Path(path) / package_name.split('.')[-1]
                if potential_path.is_dir() and (potential_path / '__init__.py').exists():
                    return potential_path

            logger.warning(
                f"Could not determine path for package {package_name}")
            return None

        except ImportError as e:
            logger.error(f"Could not import package {package_name}: {str(e)}")
            return None

    def discover_routers(self) -> None:
        """
        Discovers all router modules in the specified package.
        """
        package_path = self._get_package_path(self.base_package)

        if not package_path:
            logger.error(
                f"Could not find package path for {self.base_package}")
            # Create empty api/v1 directory if it doesn't exist
            default_path = Path(__file__).parent.parent / 'api' / 'v1'
            default_path.mkdir(parents=True, exist_ok=True)
            (default_path / '__init__.py').touch(exist_ok=True)
            package_path = default_path
            logger.info(f"Created default API directory at {default_path}")

        try:
            # Get the package spec
            for module_info in pkgutil.iter_modules([str(package_path)]):
                module_name = f"{self.base_package}.{module_info.name}"

                try:
                    # Import the module
                    module = importlib.import_module(module_name)

                    # Find all APIRouter instances in the module
                    for name, obj in inspect.getmembers(module):
                        if isinstance(obj, APIRouter):
                            endpoint_prefix = module_info.name
                            self._discovered_routers.append(
                                (endpoint_prefix, obj))
                            logger.info(
                                f"Discovered router in module: {module_name}")

                except Exception as e:
                    logger.error(
                        f"Error importing module {module_name}: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error discovering routers: {str(e)}")
            return

    def register_routers(self) -> None:
        """
        Registers all discovered routers with the FastAPI application.
        """
        if not self._discovered_routers:
            logger.warning("No routers discovered to register")
            return

        for endpoint_prefix, router in self._discovered_routers:
            try:
                formatted_prefix = endpoint_prefix.replace('_', '-')

                self.app.include_router(
                    router,
                    prefix=f"{settings.API_V1_STR}/{formatted_prefix}",
                    tags=[formatted_prefix]
                )
                logger.info(
                    f"Registered router with prefix: {formatted_prefix}")

            except Exception as e:
                logger.error(
                    f"Error registering router for {endpoint_prefix}: {str(e)}")

    def setup(self) -> None:
        """
        Complete setup process with error handling.
        """
        try:
            self.discover_routers()
            self.register_routers()
        except Exception as e:
            logger.error(f"Error during router setup: {str(e)}")
            # Continue application startup even if router registration fails
            pass
