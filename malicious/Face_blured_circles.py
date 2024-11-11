import cv2 as cv

img = cv.imread('img/YBBL1387.JPG')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
height, width = img.shape[:2]
img = cv.GaussianBlur(img, (9, 9), 0)
print(height, width)

for i in range(height):
    if i % 2 == 0:
        cv.circle(img, (width//2, height//2), 1+i*3, (255, 255, 255))
    else:
        pass

cv.imshow('Test image', img)
cv.waitKey(0)
cv.destroyAllWindows()
