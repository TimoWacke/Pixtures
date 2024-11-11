import numpy as np
import cv2
from PIL import Image
import time
import cython
import matplotlib.pyplot as plt
import pyximport
pyximport.install(setup_args={"script_args" : ["--verbose"]})
import cy_import


if __name__ == "__main__":
    # lädt image in BGR format WICHTIG
    img = cv2.imread('img/city-map-src.png',cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    time_start = time.time()
    img = threshold_fast(100, img)
    print("time elapsed: {:.2f}s".format(time.time() - time_start))
    plt.imshow(img)
    plt.show()







    # print(img.shape)
    # imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
    # (h, s, v) = cv2.split(imghsv)
    # s = s * 0.5
    # imghsv = cv2.merge([h, s, v])
    # img = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    # cv2.imwrite('test.png',img)

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