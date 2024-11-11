from random import randrange
import numpy as np
from PIL import Image

import re
import time
import logging


logger = logging.getLogger(__name__)


# linear mathematics overblending 2 numbers by opacity
def blVl(o, n, opac):
    return round((o * opac * n + (1-opac) * n))


# pixel touple overblending
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
    pixel = pattern["pixels"][x, y]
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
        pix[i] = round(pix[i] * saturation + (sum(pix) / len(pix)) * (1 - saturation))
    return (pix[0], pix[1], pix[2], 255)


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
    return (round(min(255, pixel[0] * factor)),
            round(min(255, pixel[1] * factor)),
            round(min(255, pixel[2] * factor)),
            pixel[3])


class MapFace():

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.patterns, self.patternfilelist = [], []
        self.chosen_count = {}

        patternnames = {"nature": 5, "simple": 6, "hand": 16}

        for category in patternnames:
            for i in range(1, patternnames[category] + 1):
                self.patternfilelist.append(f'{category}{str(i)}.png')

        self.min_edge_size = 1080

        self.pat_size = min(350, round(self.min_edge_size / 15))  # should be an even number

        self.do_filter = True

        self.colors = {
            "buildings": [64, 64, 64],  # gray
            "parks": [81, 85, 63],  # green
            "water": [166, 192, 201]  # blue
        }

        for file in self.patternfilelist:
            try:
                try:
                    pat = Image.open("/pixtures/patterns/" + file)
                except Exception:
                    path = "patterns/"
                    pat = Image.open(path + file)

                pat = pat.resize((self.pat_size, self.pat_size))
                paxels = pat.load()
                h = 0
                count = 0
                for x in range(pat.size[0]):
                    for y in range(pat.size[1]):
                        pax = paxels[x, y]
                        opac = pax[3] / 255
                        h += (pax[0] + pax[1] + pax[2]) / 3 * opac + 255 * (1 - opac)
                        count += 1
                h /= count * 255
                self.chosen_count[file] = 0
                self.patterns.append({"brightness": h, "pixels": paxels, "type": re.findall(
                    r'(\S+)\d+\.png', file)[0], "name": file})
            except Exception:
                self.logger.info("without pattern:", file)

    # gives you the pattern with the nearest average brightness to your desired brightness (0-1)
    def getMatchingPattern(self, typeList, bright):
        bright += randrange(-10, 10) / 100
        minpattern = sorted(filter(
            lambda d: d["type"] in typeList, self.patterns),
            key=lambda item: item["brightness"],
            reverse=True)[0]
        for pattern in self.patterns:
            if pattern["type"] in typeList:
                if pattern["brightness"] > bright and pattern["brightness"] < minpattern["brightness"]:
                    minpattern = pattern

        self.chosen_count[minpattern["name"]] += 1
        return minpattern

    def run(self, im: Image, pt: Image) -> Image:

        start_time = time.time()

        imRatio = im.size[0] / im.size[1]  # > 1 for horizontal
        ptRatio = pt.size[0] / pt.size[1]  # > 1 for horizontal
        pt2imW = max(ptRatio * im.size[1], im.size[0])
        pt2imH = max(im.size[0] / ptRatio, im.size[1])

        pt = pt.resize((round(pt2imW), round(pt2imH)))
        left = round((pt2imW-im.size[0])/2)
        top = round((pt2imH-im.size[1])/2)
        right = round((im.size[0] + (pt2imW-im.size[0])/2))
        bottom = round((im.size[1] + (pt2imH-im.size[1])/2))
        pt = pt.crop((left, top, right, bottom))
        pt = pt.resize((
            round(max(self.min_edge_size, self.min_edge_size*imRatio)),
            round(max(self.min_edge_size, self.min_edge_size / imRatio))
        ))
        im = im.resize((
            round(max(self.min_edge_size, self.min_edge_size * imRatio)),
            round(max(self.min_edge_size, self.min_edge_size / imRatio))
        ))

        pixels = im.load()
        portix = pt.load()
        xwidth = pt.size[0]
        ywidth = pt.size[1]
        clusters = []
        curr = []
        clustered = np.zeros(shape=(xwidth, ywidth))

        self.logger.info("--- %s seconds ---" % (time.time() - start_time))
        # self.logger.info(patterns)
        start_time = time.time()
        self.logger.info("finding clusters...")

        def colorForCluster(cluster):
            r, g, b = 0, 0, 0
            for pix in cluster["pixels"]:
                try:
                    r += portix[pix[0], pix[1]][0]
                    g += portix[pix[0], pix[1]][1]
                    b += portix[pix[0], pix[1]][2]
                except Exception:
                    self.logger.info("err:", pix[0], pix[1])
            r /= len(cluster["pixels"])
            g /= len(cluster["pixels"])
            b /= len(cluster["pixels"])
            return pfilter([r, g, b])

        # starting at a given pixel x,y it will find all neighbor pixel in cluster (if pixel is not already clustered)
        # the pixels found will be added to a cluster in the global clusters array
        # and will be marked as done in clustered numpy array
        def findCluster(x, y, dir=False, n=0, typ=False):
            c = 1
            if n > 200:
                return c
            n += 1
            if x >= xwidth or y >= ywidth:
                return c
            if clustered[x][y]:
                return c

            if typ:
                if pixelIsColor(pixels[x, y], self.colors[typ], 15):
                    clustered[x][y] = True
                    curr["pixels"].append([x, y])
                else:
                    return c
            else:
                for color in self.colors:
                    if pixelIsColor(pixels[x, y], self.colors[color], 15):
                        typ = color
                        curr["typ"] = typ
                        clustered[x][y] = True
                        curr["pixels"].append([x, y])
                        break
                if not typ:
                    return c

            if dir:
                c += findCluster(x, y+1, "up", n, typ)
                c += findCluster(x+1, y, "right", n, typ)
                c += findCluster(x, y-1, "down", n, typ)
                c += findCluster(x-1, y,  "left", n, typ)
                return c
            if dir != "up":
                c += findCluster(x, y-1, "down", n, typ)
            if dir != "right":
                c += findCluster(x-1, y,  "left", n, typ)
            if dir != "down":
                c += findCluster(x, y+1, "up", n, typ)
            if dir != "left":
                c += findCluster(x+1, y, "right", n, typ)
            return c

        x = 0
        count_clustered_pixel = 0
        count_checked = 0
        while x < xwidth:
            y = 0
            while y < ywidth:
                if not clustered[x][y]:
                    curr = {"typ": False, "pixels": []}
                    count_checked += findCluster(x, y)
                    if curr["typ"]:
                        clusters.append(curr)
                        count_clustered_pixel += len(curr["pixels"])
                        if (len(clusters) % 1000 == 0):
                            self.logger.info(f'\tat {round(100*(x*ywidth + y) / (xwidth * ywidth))}%'
                                             f'found {len(clusters)} clusters '
                                             f'{round(100*count_checked / count_clustered_pixel)/100} c/px')
                y += 2
            x += 2

        self.logger.info(f'\t{count_clustered_pixel} pixels clustered')
        self.logger.info(f'\ton avg {round(count_clustered_pixel / len(clusters))} px per cluster')
        self.logger.info("--- %s seconds ---" % (time.time() - start_time))

        # till here is finished and working, after this is still todo

        start_time = time.time()
        self.logger.info("coloring clusters...")
        clust_counter = 0
        for clust in clusters:
            color = colorForCluster(clust)
            desiredBrightness = sum(color) / len(color) / 255
            if clust["typ"] == "buildings":
                pattern = self.getMatchingPattern(["simple"], desiredBrightness)
            elif clust["typ"] == "parks":
                pattern = self.getMatchingPattern(["nature"], desiredBrightness)
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
            # maxd = max(maxx-minx, maxy-miny)
            xo = randrange(round(self.pat_size / 2))
            yo = randrange(round(self.pat_size / 2))
            for pix in clust["pixels"]:
                x = pix[0] - minx
                y = pix[1] - miny

                x += xo
                y += yo
                x = x % self.pat_size
                y = y % self.pat_size
                try:
                    if clust["typ"] == "parks":
                        pixels[pix[0], pix[1]] = getPatternPixel(pattern, x, y, self.colors["parks"])
                    else:
                        pixels[pix[0], pix[1]] = pixelShiftBrightness(getPatternPixel(pattern, x, y, color), factor)
                except Exception as e:
                    self.logger.info(x, y)
                    raise e

            clust_counter += 1
            if clust_counter % 1000 == 0:
                self.logger.info(f'\t{round(clust_counter / len(clusters) * 100)}% done')

        self.logger.info("--- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        if self.do_filter:
            self.logger.info("applying filters...")
            for x in range(xwidth):
                for y in range(ywidth):
                    pixels[x, y] = self.greenTransparent(pixels[x, y], portix[x, y])
            self.logger.info("--- %s seconds ---" % (time.time() - start_time))

        self.logger.info("saving...")
        for pat in self.chosen_count:
            if self.chosen_count[pat] > 0:
                self.logger.info(f'\t {pat}: {self.chosen_count[pat]}')

        return im

    def greenTransparent(self, pixel, portel):
        portel = pfilter([portel[0], portel[1], portel[2]])
        opacity = 0.15
        if pixelIsColor(pixel, (255, 255, 255), 15):
            opacity = 0
        if pixelIsColor(pixel, (0, 0, 0), 1):
            opacity = 0.15
        if pixelIsColor(pixel, self.colors["water"], 10):
            opacity = 0.15
        if pixelIsColor(pixel, self.colors["parks"], 10):
            opacity = 0.4

        pix = [pixel[0] * (1-opacity) + portel[0] * opacity,
               pixel[1] * (1-opacity) + portel[1] * opacity,
               pixel[2] * (1-opacity) + portel[2] * opacity]

        contrast = 0.8
        for i, p in enumerate(pix):
            pix[i] = max(min(255, round(p * contrast + 255 * (1-contrast) / 2)), 0)
        return (pix[0], pix[1], pix[2], 255)
