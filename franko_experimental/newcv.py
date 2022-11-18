import numpy as np
import cv2


img = cv2.imread('img/city-map-src.png')
print(img.shape)

img2 = img.reshape((-1,3))
print(img2.shape)

for pix in img2:
    print(pix)