
from audioop import avg
from math import sqrt
from random import randrange
import numpy as np
from PIL import Image
import re
import sys

patterns = []

patternnames = {"nature":5, "simple": 5}
patternfilelist = []

for category in patternnames:
    for i in range(1, patternnames[category] + 1):
        patternfilelist.append(category + str(i) + ".png")



for file in patternfilelist:
    pat = Image.open("patterns/" + file)
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
    patterns.append({"brightness": h, "pixels": paxels, "type": re.findall(r'(\S+)\d+\.png', file)[0]})
    


def getMatchingPattern(type, bright):
    typeList= [type]
    minpattern = sorted(filter(lambda d: d["type"] in typeList, patterns), key=lambda item: item["brightness"],reverse=True)[0]
    for pattern in patterns:
        if pattern["brightness"] > bright and bright < minpattern["brightness"]:
            minpattern = pattern
    return minpattern

def getPatternPixel(pattern, x, y, offsetx, offsety, color):
    pixel = pattern["pixels"][x%100 + offsetx, y%100 + offsety] 
    if pixelIsColor(pixel, [255, 255,255], 15):
        return (color[0], color[1], color[2], 255)
    return pixel


def pixelIsColor(pixel, color, tolerance):
    i = 0
    for c in pixel:
        if i < 3:
            if c > color[i] + tolerance or c < color[i] - tolerance:
                return False
        i += 1
    return True

def pfilter(pix):
    saturation = 0.8
    for i in range(3):
        pix[i] = round(pix[i] * saturation + (sum(pix) / len(pix)) * (1- saturation))
    return (pix[0], pix[1], pix[2], 255)

def greenTransparent(pixel, portel):
    pix = [0, 0 ,0]
    if not pixelIsColor(pixel, (255, 255, 255), 15):
        opacity = 0.3
    else: 
        opacity = 0.2
    pix = [pixel[0] * (1-opacity) + portel[0] * opacity,
    pixel[1] * (1-opacity) + portel[1] * opacity,
    pixel[2] * (1-opacity) + portel[2] * opacity]
    return pfilter(pix)


try:
    im = Image.open("img/" + sys.argv[1] + ".png")
except:
    im = Image.open("img/amsterdam.png")
try:
    pt = Image.open("img/" + sys.argv[2])
except:
    pt = Image.open("img/portrait.png")
try:
    exportfile = "img/" + sys.argv[1] + "edit_merged.png"
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
im = im.resize((round(2000*ratio),2000))
pt = pt.resize((round(2000*ratio),2000))


pixels = im.load()
portix = pt.load()

xwidth = pt.size[0]
ywidth = pt.size[1]

clusters = []
curr = []
clustered = np.zeros(shape=(xwidth, ywidth))


def findCluster(x,y, dir=False, n=0):
    if n>200:
        return
    n+=1;
    if x >= xwidth or y >= ywidth:
        return
    if clustered[x][y]:
        return
    if pixelIsColor(pixels[x, y], (65, 65, 65), 15):
        clustered[x][y] = True;
        curr.append([x, y])
    else:
        return

    if dir != "up":
        findCluster(x,y-1,"down", n)
    if dir != "right" :
        findCluster(x-1,y,  "left", n)
    if dir != "down" :
        findCluster(x,y+1, "up", n) 
    if dir != "left" :
        findCluster(x+1,y, "right", n)

        
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
    for pix in cluster:
        try:
            r += portix[pix[0], pix[1]][0]
            g += portix[pix[0], pix[1]][1]
            b += portix[pix[0], pix[1]][2]
        except:
            print("err:", pix[0], pix[1] )
    r /= len(cluster)
    g /= len(cluster)
    b /= len(cluster)
    return pfilter([r,g,b])

print("finding clusters")
print("x:", xwidth, "y:", ywidth)
for x in range(xwidth):
    for y in range(ywidth):
        if (not clustered[x][y]) and pixelIsColor(pixels[x, y], (65, 65, 65), 15):
            curr = []
            findCluster(x,y)
            clusters.append(curr)
            if(len(clusters) % 1000 == 0):
                print("\tfound", len(clusters))





print("coloring clusters...")

for clust in clusters:
    color = colorForCluster(clust)
    desiredBrightness = sum(color) / len(color) / 255
    pattern = getMatchingPattern("simple", desiredBrightness)
    factor = desiredBrightness / pattern["brightness"]
    offsetx = randrange(-10, 10)
    offsety = randrange(-10, 10)
    for pix in clust:
        pixels[pix[0], pix[1]] = pixelShiftBrightness(getPatternPixel(pattern, pix[0], pix[1], offsetx, offsety, color), factor) 
        
x=0;
while x < xwidth:   
    y=0;
    while y < ywidth:
       
        pixels[x,y] = greenTransparent(pixels[x, y], portix[x, y])
        y += 1
    x += 1

print("saving...")
im.save(exportfile)

