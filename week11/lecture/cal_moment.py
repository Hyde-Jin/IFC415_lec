import cv2 as cv
import numpy as np
import threading, time
import SDcar 

def cal_moment(img, i, j):
    M = 0
    for a in range(img.shape[0]):
        for b in range(img.shape[1]):
            M += (a)**j * (b)**i * img[a, b]
    return M

img = cv.imread("img/line1.png", cv.IMREAD_GRAYSCALE)

if img is not None:
    print('img shape : ', img.shape)

    cv.imshow('img', img)
    y, x = img.shape
    print(' x = {}, y = {}' .format(x, y))
    y_u = int(y / 3)

    img_seg1 = img[:y_u, :]
    img_seg2 = img[y_u:y_u * 2, :]
    img_seg3 = img[y_u * 2:y_u * 3, :]
    cv.imshow("img_seg1", img_seg1)
    cv.imshow("img_seg2", img_seg2)
    cv.imshow("img_seg3", img_seg3)

    sum_val = 0

    M_seg1 = [cal_moment(img_seg1, 0, 1), cal_moment(img_seg1, 1, 0)/cal_moment(img_seg1, 0, 0), cal_moment(img_seg1, 0, 1)/cal_moment(img_seg1, 0, 0)]
    M_seg2 = [cal_moment(img_seg2, 0, 1), cal_moment(img_seg2, 1, 0)/cal_moment(img_seg2, 0, 0), cal_moment(img_seg2, 0, 1)/cal_moment(img_seg2, 0, 0)]
    M_seg3 = [cal_moment(img_seg3, 0, 1), cal_moment(img_seg3, 1, 0)/cal_moment(img_seg3, 0, 0), cal_moment(img_seg3, 0, 1)/cal_moment(img_seg3, 0, 0)]

    print('M_seg1', M_seg1)
    print('M_seg2', M_seg2)
    print('M_seg3', M_seg3)

    cv.waitKey(0)
    cv.destroyAllWindows