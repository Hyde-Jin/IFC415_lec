import cv2
import numpy as np

# Face cascade classifier 초기화
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# 웹캠 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
        
    # 프레임 상하좌우 반전
    frame = cv2.flip(frame, -1)
    
    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray)
    
    # 검출된 얼굴 수 표시
    cv2.putText(frame, f'Faces detected: {len(faces)}', 
                (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.3, (0, 255, 0), 2)
    
    # 각 얼굴에 대해 사각형 검출
    for (x, y, w, h) in faces:
        # 얼굴 사각형 그리기
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # 결과 표시
    cv2.imshow('Face Detection', frame)
    
    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()