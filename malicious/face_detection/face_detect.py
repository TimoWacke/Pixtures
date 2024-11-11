#!/usr/bin/env python3
import cv2
import sys
from PIL import Image

# functions used for debugging and extra features
# not functionally relevant for the rest of the script

# blurs image if necessary


def gaussian_blur(image, px1, px2):
    # px1 and 2 should be uneven numbers
    blurred_image = cv2.GaussianBlur(image, (px1, px2), 0)
    return blurred_image

# shows dimensions of a given image


def show_format(image):
    (h, w, c) = image.shape[:3]

    print("width: {} pixels".format(image.shape[1]))
    print("height: {} pixels".format(image.shape[0]))
    print("channels: {} pixels".format(image.shape[2]))

# shows image in pop-up window


def show_image(txt, img):
    cv2.imshow(f"{txt}", img)
    cv2.waitKey(0)
# _____________________________________________________


imagePath = sys.argv[1]
img = Image.open(sys.argv[1])
dimensions = img.size
pixels = img.load()


cascPath = "haarcascade_frontalface_default.xml"

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# Detect faces in the image
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(30, 30)

)

print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    print(x, x+w, y, y+h)
    # print(dimensions)
    # show_format(image)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if i > x and i < x+w and j > y and j < y+h:
                pix = pixels[i, j]
                if j % 100 == 0:
                    print(pix)

img.save("image_whiteout.png")
show_image("Faces found!", image)
