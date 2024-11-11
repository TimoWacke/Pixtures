#!/usr/bin/env python3
import cv2
import sys

image = cv2.imread(sys.argv[1])
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(image, (9, 9), 0)
canny = cv2.Canny(image, 50, 150)
# canny2 =


def show_format():
    (h, w, c) = image.shape[:3]

    print("width: {} pixels".format(image.shape[1]))
    print("height: {} pixels".format(image.shape[0]))
    print("channels: {} pixels".format(image.shape[2]))


def show_image(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)


show_image(canny)
