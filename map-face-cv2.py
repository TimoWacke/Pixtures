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
from npindex import npidx

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
            city_im = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
            return city_im
        except:
            # if the image is not found use the standard image
            city_im = cv2.imread("img/city-map-src.png", cv2.IMREAD_UNCHANGED)
            return city_im
    if (typ == "user"):
        try:
            # read the user portrait
            user_pt = cv2.imread("/root/Pixtures/img/" + sys.argv[2], cv2.IMREAD_UNCHANGED)
            # user_pt =  ImageOps.exif_transpose(user_pt) here we need an alternative
            # alternative for ImageOps.exif_transpose(user_pt) 
            return user_pt
        except:
            # if the user portrait is not found use the standard image
            user_pt = cv2.imread("img/portrait-src.png", cv2.IMREAD_UNCHANGED)
            return user_pt

# This function returns export image path
def get_export_path():            
    try:
        exportfile = sys.argv[1][:-4] + sys.argv[2]
        return exportfile
    except:
        exportfile = "img/edit_merged.png"
    return exportfile

#prints height and width of the image which are flipped compared to Pillow
def print_dimension(im):
    print(f'Height: {im.shape[0]}')
    print(f'Width: {im.shape[1]}')
    print(f'Channels: {im.shape[2]}')

# this function is used to get the minimum edge size of the image
def getminEdgeSize():
    try:
        minEdgeSize = int(sys.argv[3])
    except:
        minEdgeSize = 2750
    return minEdgeSize

# This function is used to resize the two images together, based on given parameters. 
def resize_images():
    minEdgeSize = getminEdgeSize()
    imRatio = pixels.shape[0] / pixels.shape[1] # > 1 for horizontal
    ptRatio = portix.shape[0] / portix.shape[1] # > 1 for horizontal
    pt2imW = max(ptRatio * pixels.shape[1], pixels.shape[0])
    pt2imH = max(pixels.shape[0] / ptRatio, pixels.shape[1])

    cv2.resize(portix, ((round(pt2imW), round(pt2imH))))
    left =round((pt2imW-pixels.shape[0])/2)
    top = round((pt2imH-pixels.shape[1])/2)
    right = round((pixels.shape[0] + (pt2imW-pixels.shape[0])/2 ))
    bottom = round((pixels.shape[1] +(pt2imH-pixels.shape[1])/2))
    portix = portix[top:bottom,left:right]
    cv2.resize(portix, (round(max(minEdgeSize, minEdgeSize*imRatio)),round(max(minEdgeSize, minEdgeSize / imRatio))))
    cv2.resize(pixels, (round(max(minEdgeSize, minEdgeSize*imRatio)),round(max(minEdgeSize, minEdgeSize / imRatio))))

# start of main function
if __name__ == '__main__':


    colors = {
    "buildings": [64, 64, 64], #gray
    "parks": [81, 85, 63], #green
    "water": [166, 192, 201] #blue
    }

    #  no need for im and pt since we are using cv2.imread instead of Image.open
    pixels = load_image("city")
    portix = load_image("user")
    exportfile = get_export_path()
    # im, pt = resize_images(im,pt)
    print_dimension(pixels)
    # cv2.imshow("city",im)
    # cv2.imshow("user", pt)
    # cv2.waitKey(0)
    exit()
    pixels = im.load()   # to recolor a pixel use: pixels[x, y] = (r, g, b, a) 
    portix = pt.load()

    # the clusters are getting created here and saved
    clusters = Cluster_Process(im).findClusters()

    # print(clusters)

    # get the fileList of patterns and load the patterns with it
    patterns, chosen_count = loadPatterns(getPatternList())

    # coloring of the clusters
    coloringClusters(pixels, portix, clusters)
    # apply filters, if you dont want this just set parameter to False
    applyFilter(im, pt, True)
    # show the patterns that were used
    # showPats()

    im.save(exportfile)
    print_dimension(im)
    print(exportfile)