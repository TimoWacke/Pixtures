
from audioop import avg
from math import *
from random import randrange
import numpy as np
from PIL import Image
import re
import sys
import time
patterns = []
chosen_count = {}

patternnames = {"nature":5, "simple": 5, "hand": 16, "nature": 5}
patternfilelist = []

for category in patternnames:
    for i in range(1, patternnames[category] + 1):
        patternfilelist.append(category + str(i) + ".png")

patsize = 700
padding = 40
minEdgeSize = 3000
doFilter = False

colors = {
"buildings": [64, 64, 64],
"parks": [81, 85, 63],
"water": [166, 192, 201]
}

def preparePattern(pat, loc, f):
    pat = pat.resize((patsize+2*padding,patsize+2*padding))
    pat = pat.crop((padding,padding, patsize+padding, patsize+padding))
    paxels = pat.load()
    for x in range(pat.size[0]):
        for y in range(pat.size[1]):
            pax = paxels[x,y]
            if pax[3] == 0:
                pax = (255, 255, 255, 255)
            paxels[x,y] = pax
    pat.save(loc + "saved-" + f)

print("preparing patterns...")
start_time = time.time()
for file in patternfilelist:
    try:
        pat = Image.open("/root/Pixtures/patterns/saved-" + file)
    except:
        try:
            path = "/root/Pixtures/patterns/" 
            pat = Image.open(path + file)
            print("\t" + file, "from scratch...")
            preparePattern(pat, path, file)
            pat = Image.open(path + "saved-" + file)
        except:
            try:
                path = "patterns/"
                pat = Image.open(path + "saved-" + file)
            except:
                pat = Image.open(path  + file)                
                print("\t" + file, "from scratch...")
                preparePattern(pat, path, file)
                pat = Image.open(path + "saved-" + file)
    pat = pat.resize((patsize, patsize))
    paxels = pat.load()
    h = 0
    count = 0
    for x in range(pat.size[0]):
        for y in range(pat.size[1]):
            pax = paxels[x,y]
            if pax[3] == 0:
                pax = (255, 255, 255, 255)
            paxels[x,y] = pax
            h += pax[0] + pax[1] + pax[2]
            count += 1
    h /= 255 * 3 * count
    chosen_count[file] = 0
    patterns.append({"brightness": h, "pixels": paxels, "type": re.findall(r'(\S+)\d+\.png', file)[0], "name": file})
    

def getMatchingPattern(typeList, bright):
    minpattern = sorted(filter(lambda d: d["type"] in typeList, patterns), key=lambda item: item["brightness"],reverse=True)[0]
    for pattern in patterns:
        if pattern["brightness"] > bright and bright < minpattern["brightness"]:
            minpattern = pattern
    chosen_count[minpattern["name"]] += 1
    return minpattern

def getPatternPixel(pattern, x, y, color):
    pixel = pattern["pixels"][x,y]
    b = (pixel[0] + pixel[1] + pixel[3]) / (3*255)
    return (color[0] * b, color[1] * b, color[2] *b, 255)

def pixelIsColor(pixel, color, tolerance):
    i = 0
    for c in pixel:
        if i < 3:
            if c > color[i] + tolerance or c < color[i] - tolerance:
                return False
        i += 1
    return True

def pfilter(pix):
    saturation = 0.7
    for i in range(3):
        pix[i] = round(pix[i] * saturation + (sum(pix) / len(pix)) * (1- saturation))
    return (pix[0], pix[1], pix[2], 255)

def greenTransparent(pixel, portel):
    pix = [0, 0 ,0]
    opacity = 0
    if pixelIsColor(pixel, (255, 255, 255), 15):
       opacity = 0
    if pixelIsColor(pixel, (0, 0, 0),1): 
       opacity = 0.1
    if pixelIsColor(pixel, colors["water"],10):
       opacity = 0.2
    pix = [pixel[0] * (1-opacity) + portel[0] * opacity,
    pixel[1] * (1-opacity) + portel[1] * opacity,
    pixel[2] * (1-opacity) + portel[2] * opacity]
    return pfilter(pix)

try:
    im = Image.open(sys.argv[1])
except:
    im = Image.open("img/city-map-src.png")
try:
    pt = Image.open("/root/Pixtures/img/" + sys.argv[2])
except:
    pt = Image.open("img/portrait-src.png")
try:
    exportfile = sys.argv[1][:-4] + "edit_merged.png"
except:
    exportfile = "img/edit_merged.png"

ratio = pt.size[0] / pt.size[1]
neww = min(im.size[0], im.size[1] * ratio)
newh = min(im.size[1], im.size[0] / ratio)
left = round((im.size[0]-neww)/2)
top = round((im.size[1]-newh)/2)
right = round((im.size[0]+neww)/2)
bottom = round((im.size[1]+newh)/2)
im = im.crop((left,top,right,bottom))
im = im.resize((round(minEdgeSize*ratio),minEdgeSize))
pt = pt.resize((round(minEdgeSize*ratio),minEdgeSize))

pixels = im.load()
portix = pt.load()
xwidth = pt.size[0]
ywidth = pt.size[1]
clusters = []
curr = []
clustered = np.zeros(shape=(xwidth, ywidth))

def findCluster(x,y, dir=False, n=0, typ=False):
    c=1
    if n>800:
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

    if not dir:
        c += findCluster(x+1,y, "right", n, typ)
        c += findCluster(x,y-1,"down", n, typ)
        c += findCluster(x,y+1, "up", n, typ)
        c += findCluster(x-1,y,  "left", n, typ)
        return c
    if dir == "up":
        c += findCluster(x,y+1, "up",  n, typ)
        c += findCluster(x-1,y,  "left", n, typ)
        c += findCluster(x+1,y, "right", n, typ)
    elif dir == "left" :
        c += findCluster(x+1,y, "left",  n, typ)
        c += findCluster(x,y+1, "up",  n, typ)
        c += findCluster(x,y-1,"down", n, typ)
    elif dir != "down" :
        c += findCluster(x,y+1, "up",  n, typ)
        c += findCluster(x+1,y, "right",  n, typ)  
        c += findCluster(x-1,y,  "left",  n, typ)   
    elif dir != "right" :
        c += findCluster(x+1,y, "right",  n, typ)
        c += findCluster(x,y-1,"down",  n, typ)      
        c += findCluster(x-1,y,  "left",  n, typ)
        
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
    r = 0
    g = 0
    b = 0
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
        y += 10
    x += 10

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
        pattern = getMatchingPattern(["simple", "hand"], desiredBrightness)
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
    xo = randrange(patsize / 2)
    yo = randrange(patsize / 2)
    for pix in clust["pixels"]:
        x = pix[0] - minx
        y = pix[1] - miny

        if maxd >= patsize:
            x /= maxd / patsize
            y /= maxd / patsize
            x = min(patsize -1, x)
            y = min(patsize -1, y)
        elif maxd < patsize / 4 and maxd > 10:
            x *= 2
            y *= 2
            x += xo
            y += yo
            x = min(patsize -1, x)
            y = min(patsize -1, y)
        try:
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
print("\t", chosen_count)
im.save(exportfile)
print(exportfile)

