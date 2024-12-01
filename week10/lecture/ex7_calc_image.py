import numpy as np
import cv2 as cv

x = np.uint8([250, 251])
y = np.uint8([10, 4])
print(x)
print(x.shape)
print(y)
print(cv.add(x, y))
print(cv.add(x, y).shape)
print(x + y)

img1 = cv.imread('./image/ml.png')
img2 = cv.imread('./image/opencv-logo.png')
print(img1.shape)
print(img2.shape)

img2 = cv.resize(img2, (img1.shape[1], img1.shape[0]))
print(img1.shape)
print(img2.shape)

img_add = cv.add(img1, img2)
print(img_add.shape)
cv.imshow('img_add', img_add)
cv.waitKey(0)

dst = cv.addWeighted(img1, 0.7, img2, 0.3, 0)

cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()