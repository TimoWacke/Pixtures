from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from io import BytesIO
from PIL import Image
import random
import logging
import time

from app.core.settings import settings


"""
Import is intentionally incorrect, since the API used for Scraping the maps is
created in the MapAPI.Dockerfile. This same Dockerfile flattens the folder
structure between:
- api/v1/get_map.py
- hooks/map_hook.py
- core/settings.py
to them being all in the same folder
"""

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GetMapHook:
    """
    A singleton class that manages browser sessions for capturing map screenshots.

    This class maintains a single browser instance throughout its lifecycle and handles
    the creation of new tabs for each screenshot operation. It uses Selenium WebDriver
    to interact with the browser and capture screenshots of map locations.

    Attributes:
        _instance (GetMapHook): The singleton instance of the class
        driver (webdriver.Remote): The Selenium WebDriver instance
        _initialized (bool): Flag to track if the instance has been initialized

    Example:
        >>> map_hook = GetMapHook()
        >>> image, location = map_hook.screenshot(37.7749, -122.4194, 12, 800, 600)
        >>> location
        'San Francisco'
    """

    _instance = None

    def __new__(cls):
        """
        Implement the singleton pattern to ensure only one instance exists.

        Returns:
            GetMapHook: The singleton instance of the class
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.driver = None
        return cls._instance

    def __init__(self):
        """
        Initialize the GetMapHook instance and start the browser session.
        The initialization only occurs once due to the singleton pattern.
        """
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.start_session()

    def get_options(self):
        """
        Configure and return Chrome browser options.

        Returns:
            webdriver.ChromeOptions: Configured options for the Chrome WebDriver
        """
        options = webdriver.ChromeOptions()

        # Add environment-specific Chrome flags
        chrome_flags = settings.CHROME_FLAGS.split()
        for flag in chrome_flags:
            options.add_argument(flag)

        # Set binary location if specified
        chrome_bin = settings.CHROME_BIN
        if chrome_bin:
            options.binary_location = chrome_bin

        return options

    def start_session(self):
        """
        Start a new browser session using Selenium WebDriver.

        The session is configured with a page load timeout and positioned at (0,0).
        If a session fails to start, the driver is set to None.

        Raises:
            Exception: If there's an error starting the browser session
        """
        try:
            if not self.driver:
                logger.info("Starting new browser session.")
                # Use the locally installed Chromium driver
                chrome_service = Service(settings.CHROMEDRIVER_PATH)
                self.driver = webdriver.Chrome(service=chrome_service, options=self.get_options())
                self.driver.set_page_load_timeout(10)  # Limit page load to 10 seconds
                self.driver.set_window_position(0, 0)
                self.driver.execute_script("return navigator.userAgent")
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            self.driver = None
            raise

    def screenshot(self, lat: float, lng: float, zm: int, w: int, h: int,
                   max_retries=3) -> Image:
        """
        Capture a screenshot of a map location in a new browser tab.

        Opens a new tab, navigates to the specified map location, takes a screenshot,
        and then closes the tab. The main browser session remains active for future use.

        Args:
            lat (float): Latitude of the location
            lng (float): Longitude of the location
            zm (int): Zoom level of the map (higher numbers = more zoomed in)
            w (int): Width of the screenshot in pixels
            h (int): Height of the screenshot in pixels
            max_retries (int, optional): Maximum number of retries on failure. Defaults to 3.

        Returns:
            tuple: (PIL.Image, str) - The screenshot image and location name

        Raises:
            Exception: If there's an error taking the screenshot
        """
        try:
            # Ensure we have an active session
            if not self.driver:
                self.start_session()

            # Create and switch to a new tab
            self.driver.execute_script("window.open('');")
            tabs = self.driver.window_handles
            new_tab = tabs[-1]  # Get the last opened tab
            self.driver.switch_to.window(new_tab)

            # Configure tab window size
            self.driver.set_window_size(w, h)

            # Navigate to the map URL
            url = f'{settings.MAP_URL}?lat={lat}&lng={lng}&zm={zm}'
            self.driver.get(url)
            time.sleep(3)  # Allow time for map to load and render

            # Capture and process the screenshot
            screenshot_bytes = self.driver.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot_bytes))

            # Clean up: close tab and switch back to original
            self.driver.close()
            self.driver.switch_to.window(tabs[0])

            logger.info(f"Screenshot captured for coordinates {lat}, {lng}")
            return image

        except Exception as e:
            if max_retries > 0:
                # Clean up session on error
                self.cleanup()
                logger.error(f"Attempt to make screenshot failed ({max_retries} retries remaining): {e}")
                time.sleep(random.uniform(1, 3))  # Random delay between retries
                return self.screenshot(lat, lng, zm, w, h,
                                       max_retries=max_retries - 1)
            logger.error(f"Error taking screenshot: {e}.")
            raise

    def cleanup(self):
        """
        Clean up the browser session and resources.

        This method ensures that the browser session is properly closed
        and resources are released.
        """
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def __del__(self):
        """
        Destructor to ensure proper cleanup when the object is destroyed.
        """
        self.cleanup()
