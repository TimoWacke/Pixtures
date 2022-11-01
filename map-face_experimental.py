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

#x, y is the starting point of the recursive search, dir = Direction, n counts the recutsion calls 
def findCluster(x,y, dir=False, n=0, typ=False):
    c=1
    if n>200:
        return c
    n+=1
    if x >= xwidth or y >= ywidth:
        return c
    if clustered[x][y]:
        return c

    if typ:
        if pixelIsColor(pixels[x, y], colors[typ], 15):
            clustered[x][y] = True    
            curr["pixels"].append([x, y])
        else:
            return c
    else:
        for color in colors:
            if pixelIsColor(pixels[x, y], colors[color], 15):
                typ = color
                curr["typ"] = typ
                clustered[x][y] = True
                curr["pixels"].append([x, y])
                break
        if not typ:
            return c

    if  dir:
        c += findCluster(x,y+1, "up", n, typ)
        c += findCluster(x+1,y, "right", n, typ)
        c += findCluster(x,y-1,"down", n, typ)
        c += findCluster(x-1,y,  "left", n, typ)
        return c
    if dir != "up" :
        c += findCluster(x,y-1,"down", n, typ)
    if dir != "right" :
        c += findCluster(x-1,y,  "left", n, typ)
    if dir != "down":
        c += findCluster(x,y+1, "up", n, typ)
    if dir != "left" :
        c += findCluster(x+1,y, "right", n, typ)
    return c

if __name__ == '__main__':


    colors = {
    "buildings": [64, 64, 64], #gray
    "parks": [81, 85, 63], #green
    "water": [166, 192, 201] #blue
    }


    im = load_image("city")
    pt = load_image("user")
    
    
    xwidth = pt.size[0]
    ywidth = pt.size[1]

    exportfile = get_export_path()
    im, pt = resize_images(im,pt)
    pixels = im.load()   # to recolor a pixel use: pixels[x, y] = (r, g, b, a) 
    portix = pt.load()

    xwidth = pt.size[0]
    ywidth = pt.size[1]
    clusters = []
    curr = []
    clustered = np.zeros(shape=(xwidth, ywidth))

    print("finding clusters...")
    start_time = time.time()
    x=0
    count_clustered_pixel = 0
    count_checked = 0
    while x < xwidth:   
        y=0
        while y < ywidth:
            if not clustered[x][y]:
                curr = {"typ": False, "pixels": []}
                count_checked += findCluster(x,y)
                if curr["typ"]:
                    clusters.append(curr)
                    count_clustered_pixel += len(curr["pixels"])
                    if(len(clusters) % 1000 == 0):
                        print(f'\tat {round(100*(x*ywidth + y) / (xwidth * ywidth))}% found {len(clusters)} clusters {round(100*count_checked / count_clustered_pixel)/100} c/px')
            y += 2
        x += 2

    print(f'\t{count_clustered_pixel} pixels clustered')
    print(f'\ton avg {round(count_clustered_pixel / len(clusters))} px per cluster')
    print("--- %s seconds ---" % (time.time() - start_time))


    im.save(exportfile)
    print_dimension(im)
    print(exportfile)