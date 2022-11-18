import numpy as np
import cv2
from PIL import Image
import time

def saturatePixel(pix):
    # print(pix)
    # new saturation should be 0.5 of original
    alpha = 0.5
    beta = 1 - alpha
    #pix = (b, g, r, a)
    avg = (pix[0] + pix[1]+ pix[2]) / 3
    new_pix = [pix[0] * alpha + avg * beta, pix[1] * alpha + avg * beta, pix[2] * alpha + avg * beta, pix[3]]
    # for i in range(3):
    #     pix[i] = (pix[i]*sat + avg*(1-sat))
    return new_pix

if __name__ == "__main__":
    # lädt image in BGR format WICHTIG
    img = cv2.imread('img/city-map-src.png',cv2.IMREAD_UNCHANGED)
    print(img.shape)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
    (h, s, v) = cv2.split(imghsv)
    s = s * 0.5
    imghsv = cv2.merge([h, s, v])
    img = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    cv2.imwrite('test.png',img)

    # img2 = img.reshape((-1,4))
    # print(img2.shape)
    # print ("this is the first pixel of the whole image:", img2[0])



    # print("start saturation")
    # start_time = time.time() 
    # for i,val in enumerate(img2):
    #     img2[i] = saturatePixel(val)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # for pix in img2:
    #     print(pix)
    # img2 = img2.reshape(img.shape[0],img.shape[1],4)
    # cv2.imwrite('test.png',img2)