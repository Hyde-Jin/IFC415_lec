import cv2 as cv
import numpy as np
import threading, time
import SDcar
import sys
import tensorflow as tf
import RPi.GPIO as GPIO
import serial
from tensorflow.keras.models import load_model

BUZZER = 12
L_Light = 26
R_Light = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(L_Light, GPIO.OUT)
GPIO.setup(R_Light, GPIO.OUT)

# 시리얼 통신 설정
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""  # 수신 데이터 저장 변수

# 시리얼 데이터 수신 스레드 함수
def serial_thread():
    global gData, class_name, is_running
    global enable_AIdrive, enable_detection
    
    while is_running:
        try:
            data = bleSerial.readline()
            data = data.decode().strip()
            
            if data == "start_A":
                enable_AIdrive = True
            elif data == "stop_A":
                enable_AIdrive = False
                time.sleep(0.1)
                car.motor_stop()
            elif data == "start_D":
                enable_detection = True
            elif data == "stop_D":
                enable_detection = False
                class_name = None
                time.sleep(0.1)
                cv.destroyWindow('detection')
            elif data == "finish":
                is_running = False
                car.motor_stop()
                enable_AIdrive = False
                enable_detection = False
        except Exception as e:
            print(f"Serial reading error: {e}")

# 물체 감지 함수
def object_detection(image):
    global class_name

    t1 = time.time()

    image_height, image_width, _ = image.shape
    blob = cv.dnn.blobFromImage(image=image, size=(300, 300), swapRB=True)
    
    od_model.setInput(blob)
    output = od_model.forward()    

    t2 = time.time()
    print(f"operation time : {t2 - t1:.4f}s")

    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        
        if confidence > .6:
            class_id = detection[1]
            class_name = class_names[int(class_id)-1]
            color = COLORS[int(class_id)]
            
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height

            cv.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
            cv.putText(image, class_name, (int(box_x), int(box_y - 5)), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # enable_detection이 True일 때만 창을 보여줌
    if enable_detection:
        cv.imshow('detection', image)
        cv.waitKey(1)

# 물체 감지 스레드 함수
def detection_thread():
    global frame
    global is_running
    global enable_detection

    frame_count = 0
    process_interval = 30
    
    while is_running:
        current_frame = None

        if frame is not None:
            lock.acquire()
            current_frame = frame.copy()
            lock.release()

            if enable_detection and frame_count % process_interval == 0:
                try:
                    object_detection(current_frame)
                except Exception as e:
                    print(f"Error in object detection: {e}")
        
        frame_count = (frame_count + 1) % 31

# 자율주행 함수
def drive_AI(img):
    global class_name

    img = np.expand_dims(img, 0)
    res = model.predict(img)[0]
    
    steering_angle = np.argmax(np.array(res))
    print('steering_angle', steering_angle)
    
    # laptop 감지는 object detection이 활성화된 경우에만 처리
    if enable_detection and class_name == 'laptop':
        car.motor_stop()
        horn()
    else:
        # 일반적인 자율주행 로직 수행
        if steering_angle == 0:
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
        while camera.isOpened() and is_running:
            lock.acquire()
            ret, frame = camera.read()
            frame = cv.flip(frame,-1)
            lock.release()

            cv.imshow('camera', frame)
            
            crop_img = frame[int(v_y/2):,:]
            crop_img = cv.resize(crop_img, (200, 66))

            if enable_AIdrive:
                drive_AI(crop_img)

            cv.waitKey(1)

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

    # 스레드 시작
    lock = threading.Lock()
    
    # 시리얼 통신 스레드
    t_serial = threading.Thread(target=serial_thread)
    t_serial.start()
    
    # 물체 감지 스레드
    t_detection = threading.Thread(target=detection_thread)
    t_detection.start()

    # 비상등 스레드
    t_emergency = threading.Thread(target=emergency_lights)
    t_emergency.start()

    car = SDcar.Drive()
    
    main()
    
    # 프로그램 종료 처리
    is_running = False
    car.clean_GPIO()
    p.stop()
    GPIO.cleanup()
    bleSerial.close()
    print('end program')