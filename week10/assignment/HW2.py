import cv2
import numpy as np

def detect_lines(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 이진화
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    
    # 모폴로지 연산으로 노이즈 제거
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # 결과 이미지 생성
    result = image.copy()
    result[binary == 0] = 0
    
    return result, binary

image_files = [
    '/home/jin/em_lec/week10/assignment/img/img1.jpg',
    '/home/jin/em_lec/week10/assignment/img/img2.jpg',
    '/home/jin/em_lec/week10/assignment/img/img3.jpg',
    '/home/jin/em_lec/week10/assignment/img/img4.jpg'
]

num = 1
for img_path in image_files:
    result, binary = detect_lines(img_path)
    
    if result is not None and binary is not None:
        width = 480
        ratio = width / result.shape[1]
        dim = (width, int(result.shape[0] * ratio))
        
        resized_result = cv2.resize(result, dim, interpolation=cv2.INTER_AREA)
        resized_binary = cv2.resize(binary, dim, interpolation=cv2.INTER_AREA)
    
        cv2.imshow(f'Result {num}', resized_result)
        cv2.imshow(f'Binary {num}', resized_binary)
        cv2.waitKey(0)
    num += 1
        
cv2.destroyAllWindows()