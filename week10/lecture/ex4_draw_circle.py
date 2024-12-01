import numpy as np
import cv2 as cv

def draw_circle(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img, (x, y), 10, (255, 0, 0), -1)
    elif event == cv.EVENT_RBUTTONDBLCLK:
        cv.circle(img, (x, y), 10, (0, 0, 255), -1)

img = np.ones((512, 512, 3), np.uint8) * 220
cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)

while(1):
    cv.imshow('image', img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()