import threading
import serial
import RPi.GPIO as GPIO
import time

# 핀 번호 설정
PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

# 출력 주파수 설정
L_Motor = GPIO.PWM(PWMA, 250)
R_Motor = GPIO.PWM(PWMB, 250)

# 초기 정지 상태
L_Motor.start(0)
R_Motor.start(0)

# 수신 데이터 저장 변수
gData = ""

# 수신 데이터를 실시간 저장 함수
def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        data = data.decode()
        gData = data

def main():
    global gData
    try:
        while True:
            # "go"를 수신 받으면
            if gData.find("go") >= 0:
                gData = ""
                # 방향 및 속도 설정 후 출력 (전진)
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(50)
                R_Motor.ChangeDutyCycle(50)
            # "back"을 수신 받으면
            elif gData.find("back") >= 0:
                gData = ""
                # 방향 및 속도 설정 후 출력 (후진)
                GPIO.output(AIN1, 1)
                GPIO.output(AIN2, 0)
                GPIO.output(BIN1, 1)
                GPIO.output(BIN2, 0)
                L_Motor.ChangeDutyCycle(50)
                R_Motor.ChangeDutyCycle(50)
            # "left"를 수신 받으면
            elif gData.find("left") >= 0:
                gData = ""
                # 방향 및 속도 설정 후 출력 (좌회전)
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(25)
                R_Motor.ChangeDutyCycle(75)
            # "right"를 수신 받으면
            elif gData.find("right") >= 0:
                gData = ""
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(75)
                R_Motor.ChangeDutyCycle(25)
            # "stop"을 수신 받으면
            elif gData.find("stop") >= 0:
                gData = ""
                L_Motor.ChangeDutyCycle(0)
                R_Motor.ChangeDutyCycle(0)
    except KeyboardInterrupt:
        pass

# main 모듈에서만 동작
if __name__ == '__main__':
    task1 = threading.Thread(target = serial_thread)
    task1.start()
    main()
    bleSerial.close()