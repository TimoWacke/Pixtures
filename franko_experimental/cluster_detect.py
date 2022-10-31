# import cv2
# import numpy as np
# from matplotlib import pyplot as plt

# im = cv2.imread('img/city-map-src.png')
# gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# # distance-transform
# dist = cv2.distanceTransform(~gray, cv2.DIST_L1, 3)
# # max distance
# k = 10
# bw = np.uint8(dist < k)
# # remove extra padding created by distance-transform
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
# bw2 = cv2.morphologyEx(bw, cv2.MORPH_ERODE, kernel)
# # clusters
# _, contours, _ = cv2.findContours(bw2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # draw clusters and bounding-boxes
# i = 0
# print(len(contours))
# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.drawContours(im, contours, i, (255, 0, 0), 2)
#     i += 1

# plt.subplot(121); plt.imshow(im)
# plt.subplot(122); plt.imshow(bw2)

# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-c", "--clusters", required = True, type = int,
	help = "# of clusters")
args = vars(ap.parse_args())
# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# show our image
plt.figure()
plt.axis("off")
plt.imshow(image)