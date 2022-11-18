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
            city_im = cv2.cvtColor(city_im, cv2.COLOR_BGR2RGB)
            return city_im
        except:
            # if the image is not found use the standard image
            city_im = cv2.imread("img/city-map-src.png", cv2.IMREAD_UNCHANGED)
            city_im = cv2.cvtColor(city_im, cv2.COLOR_BGR2RGB)
            return city_im
    if (typ == "user"):
        try:
            # read the user portrait
            user_pt = cv2.imread("/root/Pixtures/img/" + sys.argv[2], cv2.IMREAD_UNCHANGED)
            user_pt = cv2.cvtColor(user_pt, cv2.COLOR_BGR2RGB)
            # user_pt =  ImageOps.exif_transpose(user_pt) here we need an alternative
            # alternative for ImageOps.exif_transpose(user_pt) 
            return user_pt
        except:
            # if the user portrait is not found use the standard image
            user_pt = cv2.imread("img/portrait-src.png", cv2.IMREAD_UNCHANGED)
            user_pt = cv2.cvtColor(user_pt, cv2.COLOR_BGR2RGB)
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
        minEdgeSize = 750
    return minEdgeSize

# This function is used to resize the two images together, based on given parameters. 
def resize_images(pixels, portix):
    minEdgeSize = getminEdgeSize()
    pixel_height = pixels.shape[0]
    pixel_width = pixels.shape[1]
    portix_height = portix.shape[0]
    portix_width = portix.shape[1]

    imRatio = pixel_width / pixel_height # > 1 for horizontal
    ptRatio = portix_width / portix_height # > 1 for horizontal
    pt2imW = max(ptRatio * pixel_height, pixel_width)
    pt2imH = max(pixel_width / ptRatio, pixel_height)

    cv2.resize(portix, ((round(pt2imW), round(pt2imH))))
    left =round((pt2imW-pixel_width)/2)
    top = round((pt2imH-pixel_height)/2)
    right = round((pixel_width + (pt2imW-pixel_width)/2 ))
    bottom = round((pixel_height +(pt2imH-pixel_height)/2))
    print(top, bottom, left , right)
    portix = portix[top:bottom,left:right]
    cv2.resize(portix, (round(max(minEdgeSize, minEdgeSize*imRatio)),round(max(minEdgeSize, minEdgeSize / imRatio))))
    cv2.resize(pixels, (round(max(minEdgeSize, minEdgeSize*imRatio)),round(max(minEdgeSize, minEdgeSize / imRatio))))
    return pixels, portix

# functionality needs to be defined by Timo
def pixelIsColor(pixel, color, tolerance):
    for i,c in enumerate(pixel):
        if i < 3:
            if c > color[i] + tolerance or c < color[i] - tolerance:
                return False
    return True

# this is a class for the clusters
class Cluster:
    def __init__(self, typ):
        self.typ = typ
        self.pixels = []
    def addPixel(self, x, y):
        self.pixels.append([x ,y])
    def addPixels(self, pixels):
        for pix in pixels:
            self.addPixel(pix[0], pix[1])

# this function is used to find the clusters in the image
class Cluster_Process:
    def __init__(self, pixels):
        self.pixels = pixels
        self.xwidth = pixels.shape[1]
        self.ywidth = pixels.shape[0]
        self.clustered = np.zeros(shape=(self.xwidth, self.ywidth))
        self.clusters = []
    #starting at a given pixel x,y it will find all neighbor pixel in cluster (if pixel is not already clustered)
    #the pixels found will be added to a cluster in the global clusters array and will be marked as done in clustered numpy array
    def findCluster(self,x,y, dir=False, n=0, typ=False):
        pixels = self.pixels
        xwidth = self.xwidth
        ywidth = self.ywidth
        clustered = self.clustered
        foundPixels = []
        if n>200:
            return []
        n+=1
        if x >= xwidth or y >= ywidth:
            return []
        if clustered[x][y]:
            return []

        if typ:
            if pixelIsColor(pixels[x, y], colors[typ], 15):
                foundPixels.append([x, y])
                clustered[x][y] = True    
            else:
                return []
        else:
            for color in colors:
                if color != "water" and pixelIsColor(pixels[x, y], colors[color], 15):
                    typ = color
                    newCluster = Cluster(typ)
                    newCluster.addPixel(x, y)
                    clustered[x][y] = True
                    break
            if not typ:
                return []

        if not dir:
            newCluster.addPixels(Cluster_Process.findCluster(self,x,y+1, "up", n, typ))
            newCluster.addPixels(Cluster_Process.findCluster(self,x+1,y, "right", n, typ))
            newCluster.addPixels(Cluster_Process.findCluster(self,x,y-1,"down", n, typ))
            newCluster.addPixels(Cluster_Process.findCluster(self,x-1,y,  "left", n, typ))
            return newCluster 

        if dir != "up" :
            foundPixels.extend(self.findCluster(x,y-1,"down", n, typ))
        if dir != "right" :
            foundPixels.extend(self.findCluster(x-1,y,  "left", n, typ))
        if dir != "down":
            foundPixels.extend(self.findCluster(x,y+1, "up", n, typ))
        if dir != "left" :
            foundPixels.extend(self.findCluster(x+1,y, "right", n, typ))
        return foundPixels

    def findClusters(self):
        print("finding clusters...")
        start_time = time.time()
        xwidth = self.xwidth
        ywidth = self.ywidth
        clustered = self.clustered
        clusters = self.clusters
        x=0
        count_clustered_pixel = 0
        count_checked = 0
        while x < xwidth:   
            y=0
            while y < ywidth:
                if not clustered[x][y]:
                    newclust = Cluster_Process.findCluster(self,x,y)
                    if newclust != []:
                        clusters.append(newclust)
                        count_clustered_pixel += len(newclust.pixels)
                        if(len(clusters) % 1000 == 0):
                            print(f'\tat {round(100*(x*ywidth + y) / (xwidth * ywidth))}% found {len(clusters)} clusters {round(100*count_checked / count_clustered_pixel)/100} c/px')
                y += 2
            x += 2
        print(f'\t{count_clustered_pixel} pixels clustered')
        print(f'\ton avg {round(count_clustered_pixel / len(clusters))} px per cluster')
        print("--- %s seconds ---" % (time.time() - start_time))
        return self.clusters

def tupleRGBA(rgbaArray):
    rgbaArray = list(map(lambda x: round(x), rgbaArray))
    if len(rgbaArray) == 4:
        return (rgbaArray[0], rgbaArray[1],rgbaArray[2],rgbaArray[3])
    return (rgbaArray[0], rgbaArray[1], rgbaArray[2], 255)

def colorForCluster(portix, cluster): 
    r, g, b = 0, 0, 0
    for pix in cluster.pixels:
        try:
            r += portix[pix[0], pix[1]][0]
            g += portix[pix[0], pix[1]][1]
            b += portix[pix[0], pix[1]][2]
        except:
            print("err:", pix[0], pix[1] )
    r /= len(cluster.pixels)
    g /= len(cluster.pixels)
    b /= len(cluster.pixels)
    return (r,g,b, 255)

# colors the clusters of given image
def coloringClusters(pixels, portix, clusters):
    # start timer
    start_time = time.time()
    print("coloring clusters...")

    # coloring clusters
    for clust_counter, clust in enumerate(clusters):
        color = colorForCluster(portix, clust)
        for pix in clust.pixels:
            if clust.typ == "parks":
                pixels[pix[0], pix[1]] =  tupleRGBA(colors["parks"])
            elif clust.typ == "water":
                pixels[pix[0], pix[1]] =  tupleRGBA(colors["water"])
            else:
                pixels[pix[0], pix[1]] = tupleRGBA(color)


        
        if clust_counter % 1000 == 0:
            print(f'\t{round(clust_counter / len(clusters) * 100)}% done')

    print("--- %s seconds ---" % (time.time() - start_time))

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
    pixels, portix = resize_images(pixels, portix)
    print_dimension(pixels)
    print_dimension(portix)
    # the clusters are getting created here and saved
    clusters = Cluster_Process(pixels).findClusters()

    # coloring of the clusters
    coloringClusters(pixels, portix, clusters)
    cv2.imwrite(exportfile, pixels)
    print(exportfile)
    exit()


    # print(clusters)

    # get the fileList of patterns and load the patterns with it
    patterns, chosen_count = loadPatterns(getPatternList())

    # apply filters, if you dont want this just set parameter to False
    applyFilter(im, pt, True)
    # show the patterns that were used
    # showPats()
