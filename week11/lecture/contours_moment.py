import cv2 as cv

src = cv.imread("img/fig_moment.png")
dst = src.copy()

gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)

cv.imshow("gray", gray)

contours, hierarchy = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

print(len(contours))

for i in contours:
    M = cv.moments(i)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    cv.circle(dst, (cX, cY), 5, (150, 240, 50), -1)
    cv.drawContours(dst, [i], 0, (0, 255, 0), 2)

cv.imshow("dst", dst)
cv.waitKey(0)
cv.destroyAllWindows()