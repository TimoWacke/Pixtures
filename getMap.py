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
import json
import math
import os

print(sys.version)

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
def startSession(w, h):
    global driver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=getOptions())
    except Exception as e:
        print(e)
        # driver = webdriver.Chrome(executable_path="//root/.wdm/drivers/chromedriver/linux64/105.0.5195.52/chromedriver",options=getOptions())
    driver.set_window_position(0,0)
    driver.set_window_size(w,h)
    #initializes the user agent
    driver.execute_script("return navigator.userAgent")
    return driver

def screenshot(lat,lng,zm, w,h, filename):

     
    driver = startSession(w, h)
    print("selenium session started")
    #searchesthe eans
    url= f'https://framed.timopictur.es/html/map.html?lat={lat}lng={lng}zm={zm}'
    print("site opened")
    driver.get(url)
    time.sleep(7)
    
    print("screenshot...")
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,\
    #     '//*[@id="content"]/div[2]/div[3]/div[1]/div/p/span')))
    #goes into xpath with price and returns text value
    driver.get_screenshot_as_file(filename)
    print("...saved as ", filename)
    driver.quit()
    print("end....")
    return url


try:
    lat=float(sys.argv[1])
    lng=float(sys.argv[2])
    zm =float(sys.argv[3])
    width=round(float(sys.argv[4]))
    height=round(float(sys.argv[5]))

    resolutionShift = max(2750 / width, 1) 
    width  *= resolutionShift
    height *= resolutionShift
    zm += math.log(resolutionShift, 2)

except Exception as e:
    print("error:", e)
    print("use stockholm")
    lat = 59.34
    lng = 18.099
    zm = 14    
    width=1800
    height=2400

geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.reverse(f'{lat}, {lng}')

address = location[0].split(", ")
state = address[len(address)-3]
county = address[len(address)-4]
city = []
for word in state.split(" "):
    for w in county.split(" "):
        if word == w:
            city.append(w)
if(len(city) == 0):
    city = county + "-" + state
else:
    city = " ".join(city)
print(city)


filename = f'/pixtures/img/{lat}_{lng}_{zm}_{width}x{height}-{city}-map.png'

try:
    if not os.path.exists(filename):
        print(screenshot(lat, lng, zm, width, height, filename))
    else:
        print("exists already")

except:
    filename = filename[len("/pixtures"):]
    print(screenshot(lat, lng, zm, width, height, filename))

print(filename)

