from selenium import webdriver
from PIL import Image
from io import BytesIO
import time
import reverse_geocoder as rg
import logging
import random

from app.core.settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GetMapHook:
    _instance = None

    def __new__(cls):
        # If an instance doesn't exist, create one
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.driver = None
        return cls._instance

    def get_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        return options

    def start_session(self):
        try:
            if not self.driver:
                logger.info("Starting new browser session.")
                self.driver = webdriver.Remote(
                    command_executor=settings.SELENIUM_URL,
                    options=self.get_options()
                )
                self.driver.set_page_load_timeout(10)  # Limit page load to 10 seconds
                self.driver.set_window_position(0, 0)
                # self.driver.set_window_size(3840, 2160)
                self.driver.execute_script("return navigator.userAgent")
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            self.driver = None

    def get_location_name(self, lat, lng):
        try:
            location = rg.search((lat, lng))
            return location[0]['name']
        except Exception as e:
            e
            # logger.error(f"Error retrieving location: {e}")
            return "Unknown Location"

    def retry_screenshot(self, lat, lng, zm, w, h, retries=3):
        for attempt in range(retries):
            try:
                return self.screenshot(lat, lng, zm, w, h)
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise  # Re-raise exception after last attempt
                time.sleep(random.uniform(1, 3))  # Random delay between retries

    def screenshot(self, lat, lng, zm, w, h):
        # Start/reuse the driver session
        self.start_session()
        self.driver.set_window_size(w, h)

        # Construct the map URL
        url = f'{settings.MAP_URL}?lat={lat}&lng={lng}&zm={zm}'
        # url = "https://airbnb.com"
        self.driver.get(url)
        time.sleep(3)  # Give the page time to load

        # Capture screenshot as bytes and convert it to a Pillow image
        screenshot_bytes = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot_bytes))  # Convert to Pillow

        self.driver.quit()  # Quit the driver after use
        self.driver = None

        logger.info(f"Screenshot captured for coordinates {lat}, {lng}")

        return image, self.get_location_name(lat, lng)
