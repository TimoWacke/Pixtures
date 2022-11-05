from math import *
from random import randrange
import numpy as np
from PIL import Image, ImageOps
import sys

try:
    pt = Image.open("/root/Pixtures/img/" + sys.argv[1])
except:
    pt = Image.open("img/portrait.png")

width = 1000;
scheme = 15;
pt = pt.resize((width, int(pt.size[1] * width / pt.size[0])))
portix = pt.load()

shrifix = np.ones(pt.size)

curr = []
csum = 0

def brightness(pix):
    if len(pix) < 3:
        return (pix[0] + pix[1] + pix[2]) / (3 * 255) * (pix[3] / 255)
    return (pix[0] + pix[1] + pix[2]) / (3 * 255)

def avgBrightness(pixels):
    ret = 0
    for pix in pixels:
        ret += brightness(pix)
    return ret / len(pixels)

i = 1
while i + 2 < pt.size[0]:
    for j in range(0, pt.size[1]):
        five = avgBrightness([portix[i-2, j], portix[i-1, j], portix[i, j] , portix[i+1, j], portix[i+2, j]])
        csum += five
        curr.append(five)
        if len(curr) > scheme:
            csum -= curr.pop(0)
        if (csum / len(curr) < 8/9 and i%2==0) or csum / len(curr) < 3/9:
            shrifix[i][j] = max(0, shrifix[i][j] - 0.8)
    i += 3

i = 2
while i + 2 < pt.size[1]:
    for j in range(0, pt.size[0]):
        five = avgBrightness([portix[j,i-2], portix[j,i-1], portix[j, i] , portix[j, i+1], portix[j, i+2]])
        csum += five
        curr.append(five)
        if len(curr) > scheme:
            csum -= curr.pop(0)
        if (csum / len(curr) < 7/9 and i%2==0) or csum / len(curr) < 4/9:
            shrifix[j][i] = max(0, shrifix[j][i] - 0.8)
    i += 3    


i = - pt.size[0]
while i < pt.size[1]:
    jstart = max(2, -i)
    for j in range(jstart, min(pt.size[0] - 2, pt.size[1] - i)):
        five = avgBrightness([portix[j-2,j+i], portix[j-1,j+i], portix[j,j+i] , portix[j+1, j+i], portix[j+2, j+i]])
        csum += five
        curr.append(five)
        if len(curr) > scheme:
            csum -= curr.pop(0)
        if (csum / len(curr) < 6/9 and i%2==0) or csum / len(curr) < 1/9:
            shrifix[j][j+i-3] = max(0, shrifix[j][j+i-3] - 0.125)
            shrifix[j][j+i-4] = max(0, shrifix[j][j+i-4] - 0.8)
            shrifix[j][j+i-5] = max(0, shrifix[j][j+i-5] - 0.125)
  
    i += 3

i = pt.size[0] + pt.size[1] - 2
while i > 0:
    jstart = max(2, i - pt.size[1] + 2)
    for j in range(jstart, min(pt.size[0]-2,i)):
        five = avgBrightness([portix[j-2,i-j], portix[j-1,i-j], portix[j,i-j] , portix[j+1, i-j], portix[j+2, i-j]])
        csum += five
        curr.append(five)
        if len(curr) > scheme:
            csum -= curr.pop(0)
        if (csum / len(curr) < 5/9 and i%2==1) or csum / len(curr) < 1/9:
            shrifix[j][i-j+1] = max(0,shrifix[j][i-j+1] - 0.125)
            shrifix[j][i-j] = max(0, shrifix[j][i-j] - 0.8)
            shrifix[j][i-j-1] = max(0, shrifix[j][i-j-1] - 0.125)

    i -= 3


im = Image.fromarray(np.uint8(np.swapaxes(shrifix, 0 ,1)*255)).convert('RGB')
im.save("faceFX-test.png")



