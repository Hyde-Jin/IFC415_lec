import numpy as np
import cv2 as cv

img = cv.imread('./image/venom.jpg')
px = img[100, 100]
print(px)

blue = img[100, 100, 0]
print(blue)

img[100, 100] = [255, 255, 255]
print(img[100, 100])

print(img.shape)
print(img.size)
print(img.dtype)

img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
face = img[150:350, 300:500]
img[0:200, 0:200] = face

cv.imshow('face', face)
cv.waitKey(0)
cv.imshow('img + face', img)
cv.waitKey(0)