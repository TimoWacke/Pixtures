from audioop import avg
from http.client import NETWORK_AUTHENTICATION_REQUIRED
from math import *
from random import randrange
from functools import wraps
import numpy as np
from PIL import Image, ImageOps
import re
import sys
import time
import cv2
"""
requirement: argv[1] is the google map image
             argv[2] is the user picture
             argv[3] is the edge length

important output :  third last is width of the image
                    second last is height of the image
                    last print is of image path
"""
