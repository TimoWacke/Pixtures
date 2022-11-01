from audioop import avg
from http.client import NETWORK_AUTHENTICATION_REQUIRED
from math import *
from random import randrange
from functools import wraps
import numpy as np
from PIL import Image, ImageOps
import glob
import re
import sys
import time
import cv2

"""
    This function is used to load a certain image either from its
    path or from the standard image. The image is then converted to
    a PIL image and returned. The image is also determined by the description we input
    while calling the function.
"""
def load_image(typ):
    if (typ == "city"):	
        try:
            # read the image
            city_im = Image.open(sys.argv[1])
            return city_im
        except:
            # if the image is not found use the standard image
            city_im = Image.open("img/city-map-src.png")
            return city_im
    if (typ == "user"):
        try:
            # read the user portrait
            user_pt = Image.open("/root/Pixtures/img/" + sys.argv[2])
            user_pt =  ImageOps.exif_transpose(user_pt)
            return user_pt
        except:
            # if the user portrait is not found use the standard image
            user_pt = Image.open("img/portrait-src.png")
            return user_pt
# This function returns export image path
def get_export_path():            
    try:
        exportfile = sys.argv[1][:-4] + sys.argv[2]
        return exportfile
    except:
        exportfile = "img/edit_merged.png"
    return exportfile
#prints height and width of the image
def print_dimension(im):
    print(str(im.size[0]))
    print(str(im.size[1]))

# This function is used to resize the two images together, based on given parameters. 
def resize_images(im,pt):
    try:
        minEdgeSize = int(sys.argv[3])
    except:
        minEdgeSize = 750
    imRatio = im.size[0] / im.size[1] # > 1 for horizontal
    ptRatio = pt.size[0] / pt.size[1] # > 1 for horizontal
    pt2imW = max(ptRatio * im.size[1], im.size[0])
    pt2imH = max(im.size[0] / ptRatio, im.size[1])

    pt = pt.resize((round(pt2imW), round(pt2imH)))
    left =round((pt2imW-im.size[0])/2)
    top = round((pt2imH-im.size[1])/2)
    right = round((im.size[0] + (pt2imW-im.size[0])/2 ))
    bottom = round((im.size[1] +(pt2imH-im.size[1])/2))
    pt = pt.crop((left,top,right,bottom))
    pt = pt.resize((round(max(minEdgeSize, minEdgeSize*imRatio)),round(max(minEdgeSize, minEdgeSize / imRatio))))
    im = im.resize((round(max(minEdgeSize, minEdgeSize*imRatio)),round(max(minEdgeSize, minEdgeSize / imRatio))))
    return im, pt


if __name__ == '__main__':

    im = load_image("city")
    pt = load_image("user")
    exportfile = get_export_path()
    im, pt = resize_images(im,pt)

    im.save(exportfile)
    print_dimension(im)
    print(exportfile)