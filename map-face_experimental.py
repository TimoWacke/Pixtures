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
# this function is used to get the minimum edge size of the image
def getminEdgeSize():
    try:
        minEdgeSize = int(sys.argv[3])
    except:
        minEdgeSize = 750
    return minEdgeSize
# This function is used to resize the two images together, based on given parameters. 
def resize_images(im,pt):
    minEdgeSize = getminEdgeSize()
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
    def __init__(self, im):
        self.pixels = im.load()
        self.xwidth = im.size[0]
        self.ywidth = im.size[1]
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
        pixels = self.pixels
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
        return self.clusters
# this function gets the directory list of patterns
def getPatternList():
    patternfilelist = []

    patternnames = {"nature":5, "simple": 6, "hand": 16}

    for category in patternnames:
        for i in range(1, patternnames[category] + 1):
            patternfilelist.append(f'{category}{str(i)}.png')
    return patternfilelist
# uses the directory-list from above to load the patterns into a dictionary
def loadPatterns(patternfilelist):
    # getting needed variables
    chosen_count = {}
    patterns = []
    minEdgeSize = getminEdgeSize()
    
    patsize = min(350, round(minEdgeSize / 15))  # should be an even number

    # start timer
    start_time = time.time()
    print("preparing patterns...")

    # load patterns - it would be nice if the OG-Dev would explain this
    for file in patternfilelist:
        try:
            try:
                pat = Image.open("/root/Pixtures/patterns/" + file)
            except:
                path = "patterns/"
                pat = Image.open(path +  file)
                
            pat = pat.resize((patsize, patsize))
            paxels = pat.load()
            h = 0
            count = 0
            for x in range(pat.size[0]):
                for y in range(pat.size[1]):
                    pax = paxels[x,y]
                    opac = pax[3] / 255
                    h += (pax[0] + pax[1] + pax[2]) / 3 * opac + 255 * (1 - opac)
                    count += 1
            h /= count * 255
            chosen_count[file] = 0
            patterns.append({"brightness": h, "pixels": paxels, "type": re.findall(r'(\S+)\d+\.png', file)[0], "name": file})
        except:
            print("without pattern:", file)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print (patterns)
    return patterns, chosen_count

def pixelIsColor(pixel, color, tolerance):
    i = 0
    for c in pixel:
        if i < 3:
            if c > color[i] + tolerance or c < color[i] - tolerance:
                return False
        i += 1
    return True

#cluster is a list of coordinates belonging to the cluster, portix is list of pixel toubles (r, g, b, a)
def colorForCluster(portix, cluster): 
    r, g, b = 0, 0, 0
    for pix in cluster["pixels"]:
        try:
            r += portix[pix[0], pix[1]][0]
            g += portix[pix[0], pix[1]][1]
            b += portix[pix[0], pix[1]][2]
        except:
            print("err:", pix[0], pix[1] )
    r /= len(cluster["pixels"])
    g /= len(cluster["pixels"])
    b /= len(cluster["pixels"])
    return (r,g,b, 1)


if __name__ == '__main__':


    colors = {
    "buildings": [64, 64, 64], #gray
    "parks": [81, 85, 63], #green
    "water": [166, 192, 201] #blue
    }


    im = load_image("city")
    pt = load_image("user")
    

    exportfile = get_export_path()
    im, pt = resize_images(im,pt)
    # pixels = im.load()   # to recolor a pixel use: pixels[x, y] = (r, g, b, a) 
    portix = pt.load()



    print("finding clusters...")
    start_time = time.time()
    clusters = Cluster_Process(im).findClusters()
    print("--- %s seconds ---" % (time.time() - start_time))
    # print(clusters)

    # get the fileList of patterns and load the patterns with it
    patterns, chosen_count = loadPatterns(getPatternList())


    im.save(exportfile)
    print_dimension(im)
    print(exportfile)