import cv2 as cv

img1 = cv.imread('./image/venom.jpg')
img2 = cv.imread('./image/logo.jpg')

rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]

img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
cv.imshow('img2gray', img2gray)
cv.waitKey(0)

_, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
cv.imshow('mask', mask)
cv.waitKey(0)

mask_inv = cv.bitwise_not(mask)
cv.imshow('mask_inv', mask_inv)
cv.waitKey(0)

img1_bg = cv.bitwise_and(roi, roi, mask = mask_inv)
img2_fg = cv.bitwise_and(img2, img2, mask = mask)

cv.imshow('img1_bg', img1_bg)
cv.waitKey(0)
cv.imshow('img2_fg', img2_fg)
cv.waitKey(0)

dst = cv.add(img1_bg, img2_fg)
img1[0:rows, 0:cols] = dst

cv.imshow('res', img1)
cv.waitKey(0)
cv.destroyAllWindows()