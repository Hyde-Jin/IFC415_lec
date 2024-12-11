import cv2 as cv
import numpy as np
import threading, time
import SDcar
import sys
import tensorflow as tf
import RPi.GPIO as GPIO
from tensorflow.keras.models import load_model

BUZZER = 12
L_Light = 26
R_Light = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(L_Light, GPIO.OUT)
GPIO.setup(R_Light, GPIO.OUT)

# 물체 감지 함수
def object_detection(image):
    global class_name

    t1 = time.time()

    image_height, image_width, _ = image.shape
    # 이미지를 300x300 blob으로 변환
    blob = cv.dnn.blobFromImage(image=image, size=(300, 300), swapRB=True)

    # 모델 입력 설정 및 추론 실행
    od_model.setInput(blob)
    output = od_model.forward()    

    # 추론 시간 확인
    t2 = time.time()
    print(f"operation time : {t2 - t1:.4f}s")

    # 감지된 객체 처리
    for detection in output[0, 0, :, :]:
        # 신뢰도 확인
        confidence = detection[2]
        
        # 신뢰도가 0.6 이상인 경우에만 처리
        if confidence > .6:
            # 클래스 id와 이름 획득
            class_id = detection[1]
            class_name = class_names[int(class_id)-1]
            color = COLORS[int(class_id)]
            
            # 영역 박스 좌표 계산
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height

            # 박스와 클래스 표시
            cv.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
            cv.putText(image, class_name, (int(box_x), int(box_y - 5)), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv.imshow('detection', image)
    cv.waitKey(1)

# 물체 감지 스레드 함수
def detection_thread():
    global frame
    global is_running
    global enable_detection

    # 프레임 처리 간격 설정
    frame_count = 0
    process_interval = 15
    
    while is_running:
        current_frame = None

        if frame is not None:
            lock.acquire()
            current_frame = frame.copy()
            lock.release()

        # 프레임이 있고 물체 감지가 활성화된 경우에만 처리
        if enable_detection and frame_count % process_interval == 0:
            try:
                object_detection(current_frame)
            except Exception as e:
                print(f"Error in object detection: {e}")
        
        frame_count = (frame_count + 1) % 31

# 키 입력 처리 함수
def key_cmd(which_key):
    global enable_AIdrive
    global enable_detection
    
    is_exit = False 

    # 키 입력 확인 및 동작 수행
    print('which_key', which_key)
    if which_key & 0xFF == 82: # 위 방향키 : 직진
        car.motor_go(speed)
    elif which_key & 0xFF == 84: # 아래 방향키 : 후진
        car.motor_back(speed)
    elif which_key & 0xFF == 81: # 좌측 방향키 : 좌회전
        car.motor_left(30)   
    elif which_key & 0xFF == 83: # 우측 방향키 : 우회전
        car.motor_right(30)            
    elif which_key & 0xFF == 32: # 스페이스바 : 정지
        car.motor_stop()
        enable_AIdrive = False
    elif which_key & 0xFF == ord('e'): # 자율주행 시작
        enable_AIdrive = True
    elif which_key & 0xFF == ord('w'): # 자율주행 종료
        enable_AIdrive = False
        car.motor_stop()
    elif which_key & 0xFF == ord('t'): # 객체 감지 시작
        enable_detection = True
    elif which_key & 0xFF == ord('r'): # 객체 감지 종료
        enable_detection = False
        cv.destroyWindow('detection')
    elif which_key & 0xFF == ord('q'): # q : 종료
        car.motor_stop()
        enable_AIdrive = False
        enable_detection = False
        is_exit = True

    return is_exit  

# 자율주행 함수
def drive_AI(img):
    global class_name

    img = np.expand_dims(img, 0)
    res = model.predict(img)[0]
    
    steering_angle = np.argmax(np.array(res))
    print('steering_angle', steering_angle)
    if class_name == 'laptop':
        car.motor_stop()
        horn()
    elif steering_angle == 0:
        speedSet = 40
        car.motor_go(speedSet)
    elif steering_angle == 1:
        speedSet = 20
        car.motor_left(speedSet)          
    elif steering_angle == 2:
        speedSet = 20
        car.motor_right(speedSet)
    else:
        print("This cannot be entered")

# 경적 출력 함수
def horn():
    p.ChangeDutyCycle(1)
    p.ChangeFrequency(659.25)
    time.sleep(0.1)
    p.ChangeFrequency(659.25)
    time.sleep(0.4)
    p.ChangeDutyCycle(0)

# 비상등 출력 함수
def emergency_lights():
    global enable_AIdrive
    global is_running
    
    while is_running:
        if enable_AIdrive:
            GPIO.output(L_Light, GPIO.HIGH)
            GPIO.output(R_Light, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(L_Light, GPIO.LOW)
            GPIO.output(R_Light, GPIO.LOW)
            time.sleep(0.5)
        else:
            GPIO.output(L_Light, GPIO.LOW)
            GPIO.output(R_Light, GPIO.LOW)
            time.sleep(0.1)

# 메인 함수
def main():
    global frame
    global class_name
    global is_running
    global enable_AIdrive
    global enable_detection

    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH,v_x) 
    camera.set(cv.CAP_PROP_FRAME_HEIGHT,v_y)
    
    try:
        while( camera.isOpened() ):
            lock.acquire()
            ret, frame = camera.read()
            frame = cv.flip(frame,-1)
            lock.release()

            cv.imshow('camera', frame)
            
            # 이미지 크롭
            crop_img = frame[int(v_y/2):,:]
            crop_img = cv.resize(crop_img, (200, 66))

            if enable_AIdrive == True:
                drive_AI(crop_img)

            # image processing end here
            is_exit = False
            which_key = cv.waitKey(1)
            if which_key > 0:
                is_exit = key_cmd(which_key)    
            if is_exit is True:
                cv.destroyAllWindows()
                break
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)

        is_running = False

if __name__ == '__main__':
    global frame
    global class_name
    global is_running
    global enable_AIdrive
    global enable_detection

    frame = None
    class_name = None
    is_running = True
    enable_AIdrive = False
    enable_detection = False
    
    p = GPIO.PWM(BUZZER, 1)
    p.start(0)

    # 카메라 해상도 설정
    v_x = 320
    v_y = 240
    v_x_grid = [int(v_x*i/10) for i in range(1, 10)]

    # COCO 클래스와 색 설정
    class_names = []
    model_path = 'my_checkpoint/lane_navigation_20241201_1705.h5'
    model = load_model(model_path)

    with open('object_detection_classes_coco.txt', 'r') as f:
        class_names = f.read().split('\n')
    print(class_names)
    COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

    od_model = cv.dnn.readNetFromTensorflow(model='frozen_inference_graph.pb', config='ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

    # 물체 감지 스레드
    lock = threading.Lock()
    t_detection = threading.Thread(target = detection_thread)
    t_detection.start()

    # 비상등 스레드
    t_emergency = threading.Thread(target=emergency_lights)
    t_emergency.start()

    car = SDcar.Drive()
    
    main()
    is_running = False
    car.clean_GPIO()
    p.stop()
    GPIO.cleanup()
    print('end vis')