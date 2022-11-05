from math import *
from random import randrange
import numpy as np
from PIL import Image, ImageOps
import glob

'''
after you open an image with myImage.open(url) you can save it's pixels in an 2d array:

myPixels = myImage.load()

myPixels  will be 2 dimensional carrying a quadtouple for every pixel.
(255, 255, 255, 255) for RGB + Opacity


'''

import re
import sys
import time

print(sys.version)

#gives you the pattern with the nearest average brightness to your desired brightness (0-1)
def getMatchingPattern(typeList, bright):
    bright += randrange(-10, 10) / 100
    minpattern = sorted(filter(lambda d: d["type"] in typeList, patterns), key=lambda item: item["brightness"], reverse=True)[0]
    for pattern in patterns:
        if pattern["type"] in typeList:
            if pattern["brightness"] > bright  and  pattern["brightness"] < minpattern["brightness"]:
                minpattern = pattern

    chosen_count[minpattern["name"]] += 1
    return minpattern

#linear mathematics overblending 2 numbers by opacity
def blVl(o, n, opac):
   return round((o * opac * n + (1-opac) * n))

#pixel touple overblending
def blendValue(old, new, opac=False):
    if not opac:
        opac = old[3] / 255
    return (
        blVl(old[0], new[0], opac),
        blVl(old[1], new[1], opac),
        blVl(old[2], new[2], opac),
        255)

def linearBlendValue(old, new, opac):
    return (
        old[0] * (1-opac), new[0] * opac,
        old[1] * (1-opac), new[1] * opac,
        old[2] * (1-opac), new[2] * opac,
        255)

def getPatternPixel(pattern, x, y, color):
    pixel = pattern["pixels"][x,y]
    return blendValue(pixel, color)


def pixelIsColor(pixel, color, tolerance):
    i = 0
    for c in pixel:
        if i < 3:
            if c > color[i] + tolerance or c < color[i] - tolerance:
                return False
        i += 1
    return True

def pfilter(pix):
    saturation = 0.5
    for i in range(3):
        pix[i] = round(pix[i] * saturation + (sum(pix) / len(pix)) * (1- saturation))
    return (pix[0], pix[1], pix[2], 255)


def greenTransparent(pixel, portel):
    portel = pfilter([portel[0], portel[1], portel[2]])
    opacity = 0.15
    if pixelIsColor(pixel, (255, 255, 255), 15):
       opacity = 0
    if pixelIsColor(pixel, (0, 0, 0),1): 
       opacity = 0.15
    if pixelIsColor(pixel, colors["water"],10):
       opacity = 0.15
    if pixelIsColor(pixel, colors["parks"],10):
       opacity = 0.4
    
    pix = [pixel[0] * (1-opacity) + portel[0] * opacity,
    pixel[1] * (1-opacity) + portel[1] * opacity,
    pixel[2] * (1-opacity) + portel[2] * opacity]

    contrast = 0.8
    for i, p in enumerate(pix):
        pix[i] = max(min(255, round(p * contrast + 255 * (1-contrast) / 2)), 0)
    return (pix[0], pix[1], pix[2], 255)





#starting at a given pixel x,y it will find all neighbor pixel in cluster (if pixel is not already clustered)
#the pixels found will be added to a cluster in the global clusters array and will be marked as done in clustered numpy array
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
        
'''
def areaOnPixel(x,y,b=0,d=1):
    return integralOnGrid(x,y,b+d/2)-integralOnGrid(x,y,b-d/2)

def integralOnGrid(x,y,b=0):
    if x+b<y:
        return (x+1+b-y)**2 / 2;
    else:
        return 1 - (x+b-(y+1))**2 / 2

'''

def pixelShiftBrightness(pixel, factor):
    return (round(min(255, pixel[0] * factor)),round(min(255,pixel[1] * factor)), round(min(255,pixel[2] * factor)), pixel[3])


def colorForCluster(cluster):
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
    return pfilter([r,g,b])



if __name__ == "__main__":
    patterns, patternfilelist = [],[]
    chosen_count = {}

    patternnames = {"nature":5, "simple": 6, "hand": 16}

    for category in patternnames:
        for i in range(1, patternnames[category] + 1):
            patternfilelist.append(f'{category}{str(i)}.png')

    try:
        minEdgeSize = int(sys.argv[3])
    except:
        minEdgeSize = 2750


    patsize = min(350, round(minEdgeSize / 15))  # should be an even number
    doFilter = True

    colors = {
    "buildings": [64, 64, 64], #gray
    "parks": [81, 85, 63], #green
    "water": [166, 192, 201] #blue
    }



    print("preparing patterns...")
    start_time = time.time()
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
            
    try:
        im = Image.open(sys.argv[1])
    except:
        im = Image.open("img/city-map-src.png")
    try:
        pt = Image.open("/root/Pixtures/img/" + sys.argv[2])
        pt =  ImageOps.exif_transpose(pt)
    except:
        pt = Image.open("img/portrait-src.png")
    try:
        exportfile = sys.argv[1][:-4] + sys.argv[2]
    except:
        exportfile = "img/edit_merged.png"

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


    pixels = im.load()
    portix = pt.load()
    xwidth = pt.size[0]
    ywidth = pt.size[1]
    clusters = []
    curr = []
    clustered = np.zeros(shape=(xwidth, ywidth))

    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    print("finding clusters...")

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
    start_time = time.time()
    print("coloring clusters...")
    clust_counter = 0
    for clust in clusters:
        color = colorForCluster(clust)
        desiredBrightness = sum(color) / len(color) / 255
        if clust["typ"] == "buildings":
            pattern = getMatchingPattern(["simple"], desiredBrightness)
        elif clust["typ"] == "parks":
            pattern = getMatchingPattern(["nature"], desiredBrightness)
        else:
            continue
        factor = desiredBrightness / pattern["brightness"]
        maxx = 0
        maxy = 0
        minx = xwidth
        miny = ywidth
        for pix in clust["pixels"]:
            if pix[0] > maxx:
                maxx = pix[0]
            if pix[0] < minx:
                minx = pix[0]
            if pix[1] > maxy:
                maxy = pix[1]
            if pix[1] < miny:
                miny = pix[1]
        maxd = max(maxx-minx, maxy-miny)
        xo = randrange(round(patsize / 2))
        yo = randrange(round(patsize / 2))
        for pix in clust["pixels"]:
            x = pix[0] - minx
            y = pix[1] - miny
    
            x += xo
            y += yo
            x = x % patsize
            y = y % patsize 
            try:
                if clust["typ"] == "parks":
                    pixels[pix[0], pix[1]] = getPatternPixel(pattern, x, y, colors["parks"])
                else:
                    pixels[pix[0], pix[1]] = pixelShiftBrightness(getPatternPixel(pattern, x, y, color), factor) 
            except Exception as e:
                print(x,y)
                raise e
        
        clust_counter += 1
        if clust_counter % 1000 == 0:
            print(f'\t{round(clust_counter / len(clusters) * 100)}% done')

    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    if doFilter:                
        print("applying filters...")
        for x in range(xwidth):   
            for  y in range(ywidth):     
                pixels[x,y] = greenTransparent(pixels[x, y], portix[x, y])
        print("--- %s seconds ---" % (time.time() - start_time))

    print("saving...")
    for pat in chosen_count:
        if chosen_count[pat] > 0:
            print(f'\t {pat}: {chosen_count[pat]}')
    im.save(exportfile)
    print(im.size[0]) #print width as handover
    print(im.size[1]) #print height as handover
    print(exportfile)
