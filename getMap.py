from codecs import latin_1_decode
from http.client import TEMPORARY_REDIRECT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from geopy.geocoders import Nominatim
import sys
import time
import os
#some standard imports

#used for standard options
def getOptions():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    #user_ agent is used to simulate a non-headless browser, to avoid access denial
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=1')
    options.add_argument("--disable-3d-apis")
    return options

#startSession() is used to keep the browser open through global 
def startSession():
    global driver
    driver = webdriver.Chrome(executable_path="//root/.wdm/drivers/chromedriver/linux64/105.0.5195.52/chromedriver",options=getOptions())
    driver.set_window_position(0,0)
    driver.set_window_size(3500,3500)
    #initializes the user agent
    driver.execute_script("return navigator.userAgent")
    return driver

def screenshot(lat,lng,zm, filename):
    startSession()
    print("selenium session started")
    #searchesthe eans
    url= f'https://framed.timopictur.es/html/map.html?lat={lat}lng={lng}zm={zm}'
    print("site opened")
    driver.get(url)
    time.sleep(3)
    
    print("screenshot...")
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,\
    #     '//*[@id="content"]/div[2]/div[3]/div[1]/div/p/span')))
    #goes into xpath with price and returns text value
    driver.get_screenshot_as_file(filename)
    print("...saved")
    driver.quit()
    print("end....")
    return url



lat=sys.argv[1]
lng=sys.argv[2]
zm =sys.argv[3]


geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.reverse(lat + "," + lng)
city = location.raw['address'].get('city')
print(city)

filename = f'/root/Pixtures/img/{lat}_{lng}_{zm}-{city}-map.png'

if not os.path.exists(filename):
    print(screenshot(lat, lng, zm, filename))
else:
    print("exists already")
    print(city)