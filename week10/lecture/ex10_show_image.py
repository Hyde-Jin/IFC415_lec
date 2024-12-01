import cv2

img_file = "./image/img_1.png"
img = cv2.imread(img_file)

if img is not None:
    img_resize = cv2.resize(img, (960, 540))
    
    cv2. imshow("IMG", img_resize)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("Image file not found")