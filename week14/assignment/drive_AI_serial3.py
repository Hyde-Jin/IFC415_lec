# 필요한 라이브러리 임포트
import cv2 as cv
import numpy as np
import threading, time
import SDcar
import sys
import tensorflow as tf
import RPi.GPIO as GPIO
import serial
from tensorflow.keras.models import load_model

# GPIO 핀 번호 설정
BUZZER = 12  # 부저 핀
L_Light = 26  # 왼쪽 비상등 핀
R_Light = 16  # 오른쪽 비상등 핀

# GPIO 초기화
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(L_Light, GPIO.OUT)
GPIO.setup(R_Light, GPIO.OUT)

# 시리얼 통신 설정
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""  # 수신 데이터 저장 변수

# 전역 변수 초기화
frame = None  # 카메라 프레임
class_name = None  # 감지된 물체 이름
is_running = True  # 프로그램 실행 상태
enable_AIdrive = False  # 자율주행 활성화 여부
enable_detection = False  # 물체 감지 활성화 여부
enable_music = False  # 음악 재생 상태
current_note_index = 0  # 현재 재생 중인 음표 인덱스
last_note_time = 0  # 마지막으로 음표가 변경된 시간

# 음계 사전 정의
notes_dict = {
    'Do': 261.63,
    'Di' : 277.18,
    'Re': 293.66,
    'Ri' : 311.13,
    'Mi': 329.63,
    'Fa': 349.23,
    'Fi' : 369.99,
    'Sol': 392.00,
    'Si' : 415.30,
    'La': 440.00,
    'Li' : 466.16,
    'Ti': 493.88,
    '2Do': 523.25,
    '2Di' : 554.37,
    '2Re' : 587.33,
    '2Ri' : 622.25,
    '2Mi' : 659.25,
    '2Fa' : 698.46,
    '2Fi' : 739.99,
    '2Sol' : 783.99,
    '2Si' : 830.61,
    '2La' : 880.00,
    '2Li' : 932.33,
    '2Ti' : 987.77
 }

# 노래 데이터 정의
song_scale = [
    ('2Di', 0.22), ('Rest', 0.22), ('2Di', 0.22), ('Rest', 0.22), ('2Di', 0.22), ('Rest', 0.22), ('2Di', 0.22), ('2Ri', 0.22),
    ('Rest', 0.22), ('2Ri', 0.22), ('Rest', 0.22), ('2Ri', 0.22), ('2Ri', 0.22), ('Rest', 0.22), ('2Ri', 0.22), ('Rest', 0.22),
    ('Si', 0.22), ('Rest', 0.22), ('Si', 0.22), ('Rest', 0.22), ('Si', 0.22), ('Rest', 0.22), ('Si', 0.22), ('2Fa', 0.22),
    ('Rest', 0.22), ('2Fa', 0.22), ('Rest', 0.22), ('2Fa', 0.22), ('2Fa', 0.22), ('Rest', 0.22), ('2Fa', 0.22), ('Rest', 0.22)
]

# 자율주행 모델 로드
model_path = 'my_checkpoint/lane_navigation_20241201_1705.h5'
model = load_model(model_path)

with open('object_detection_classes_coco.txt', 'r') as f:
    class_names = f.read().split('\n')
print(class_names)
COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

# 물체 감지 클래스 및 모델 로드
od_model = cv.dnn.readNetFromTensorflow(
    model='frozen_inference_graph.pb',
    config='ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
)

# 시리얼 통신 스레드 함수
def serial_thread():
    global gData, class_name, is_running
    global enable_AIdrive, enable_detection, enable_music

    while is_running:
        try:
            # 시리얼 데이터 읽기
            data = bleSerial.readline().decode().strip()
            if data == "start_A":  # 자율주행 활성화 수신
                enable_AIdrive = True
            elif data == "stop_A":  # 자율주행 비활성화 수신
                enable_AIdrive = False
                time.sleep(0.1)
                car.motor_stop()
            elif data == "start_D":  # 물체감지 활성화 수신
                enable_detection = True
            elif data == "stop_D":  # 물체감지 비활성화 수신
                enable_detection = False
                class_name = None
                time.sleep(0.1)
                cv.destroyWindow('detection')
            elif data == "start_M":  # 음악 재생 활성화 수신
                enable_music = True
                p.ChangeDutyCycle(1)
            elif data == "stop_M":  # 음악 재생 비활성화 수신
                enable_music = False
                p.ChangeDutyCycle(0)
            elif data == "finish":  # 프로그램 종료 수신
                car.motor_stop()
                enable_AIdrive = False
                enable_detection = False
                p.stop()
                car.clean_GPIO()
                GPIO.cleanup()
                bleSerial.close()
                is_running = False
        except Exception as e:
            print(f"Serial reading error: {e}")

# 물체 감지 스레드 함수
def detection_thread():
    global frame, is_running, enable_detection, class_name

    frame_count = 0
    process_interval = 30  # 물체 감지 주기

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
            elif frame_count % process_interval == 0:  # detection이 꺼져있을 때만 초기화
                class_name = None
        
        frame_count = (frame_count + 1) % 31
        time.sleep(0.01)

# 음악 재생 스레드 함수
def music_thread():
    global current_note_index, last_note_time, enable_music, is_running
    
    while is_running:
        if enable_music:
            current_time = time.time()
            
            if current_note_index == 0:
                # 첫 음 재생 시 특별 처리
                note, duration = song_scale[0]
                if note != 'Rest':
                    p.ChangeFrequency(notes_dict[note])
                    p.ChangeDutyCycle(1)
                else:
                    p.ChangeDutyCycle(0)
                time.sleep(0.2)
                last_note_time = current_time
                current_note_index = 1
            
            # 현재 음표의 지속 시간이 지났는지 확인
            elif current_time - last_note_time >= song_scale[current_note_index-1][1]:
                if current_note_index < len(song_scale):
                    # 다음 음표 재생
                    note, duration = song_scale[current_note_index]

                    # 쉼표가 아닐 때만 주파수 변경
                    if note != 'Rest':
                        p.ChangeFrequency(notes_dict[note])
                        p.ChangeDutyCycle(1)
                    # 쉼표일 때는 소리를 끔
                    else:
                        p.ChangeDutyCycle(0)
                    last_note_time = current_time
                    current_note_index += 1
                else:
                    # 노래가 끝나면 처음부터 다시 시작
                    current_note_index = 0
                    last_note_time = current_time
                    p.ChangeDutyCycle(0)
        
        time.sleep(0.01)

# 자율주행 함수
def drive_AI(img):
    global class_name

    img = np.expand_dims(img, 0)
    res = model.predict(img)[0]
    steering_angle = np.argmax(np.array(res))

    # class_name 읽기 전에 lock 획득
    lock.acquire()
    current_class = class_name  # 로컬 변수에 복사
    lock.release()

    if enable_detection and current_class == 'car':
        car.motor_stop()
        horn()
    else:
        if steering_angle == 0:
            speedSet = 30
            car.motor_go(speedSet)
        elif steering_angle == 1:
            speedSet = 15
            car.motor_left(speedSet)
        elif steering_angle == 2:
            speedSet = 15
            car.motor_right(speedSet)
        else:
            print("This cannot be entered")

# 물체 감지 함수
def object_detection(image):
    global class_name
    detected = False  # 물체 감지 여부를 추적하는 플래그

    # 관심 영역(ROI) 설정
    height = int(image.shape[0] * 0.6)
    roi = image[:height, :]

    image_height, image_width, _ = roi.shape
    blob = cv.dnn.blobFromImage(image=roi, size=(160, 160), swapRB=True)
    
    # 물체 감지 수행
    od_model.setInput(blob)
    output = od_model.forward()

    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        if confidence > 0.5:
            class_id = detection[1]
            detected_class = class_names[int(class_id) - 1]
            color = COLORS[int(class_id)]

            print(f"name : {detected_class}, confidence : {confidence}")
            
            # 물체가 감지되었음을 표시
            detected = True
            class_name = detected_class

            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height

            cv.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
            cv.putText(image, detected_class, (int(box_x), int(box_y - 5)), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # 물체가 감지되지 않았다면 class_name을 None으로 초기화
    if not detected:
        class_name = None
    
    # 감지 결과를 표시
    if enable_detection:
        cv.imshow('detection', roi)
        cv.waitKey(1)

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
    global enable_AIdrive, is_running
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
    global frame, is_running

    # 카메라 초기화
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, v_x)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, v_y)
    
    try:
        while camera.isOpened() and is_running:
            lock.acquire()
            ret, frame = camera.read()
            frame = cv.flip(frame, -1)
            lock.release()

            cv.imshow('camera', frame)

            crop_img = frame[int(v_y/2):, :]
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
    # PWM 및 기타 초기화
    p = GPIO.PWM(BUZZER, 1)
    p.start(0)

    # 카메라 해상도 설정
    v_x = 320
    v_y = 240

    # 스레드 초기화 및 시작
    lock = threading.Lock()

    t_serial = threading.Thread(target=serial_thread)
    t_serial.start()

    t_detection = threading.Thread(target=detection_thread)
    t_detection.start()

    t_emergency = threading.Thread(target=emergency_lights)
    t_emergency.start()

    t_music = threading.Thread(target=music_thread)
    t_music.start()

    car = SDcar.Drive()
    
    main()

    # 종료 처리
    is_running = False