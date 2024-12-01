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

# 출력 주파수 설정
L_Motor = GPIO.PWM(PWMA, 250)
R_Motor = GPIO.PWM(PWMB, 250)

# 초기 정지 상태
L_Motor.start(0)
R_Motor.start(0)

try:
    while True:
        # 1초 간 전진
        GPIO.output(AIN1, 0)
        GPIO.output(AIN2, 1)
        GPIO.output(BIN1, 0)
        GPIO.output(BIN2, 1)
        L_Motor.ChangeDutyCycle(50)
        R_Motor.ChangeDutyCycle(50)
        time.sleep(1.0)

        # 1초 간 정지
        GPIO.output(AIN1, 0)
        GPIO.output(AIN2, 1)
        GPIO.output(BIN1, 0)
        GPIO.output(BIN2, 1)
        L_Motor.ChangeDutyCycle(0)
        R_Motor.ChangeDutyCycle(0)
        time.sleep(1.0)
except KeyboardInterrupt:
    pass

GPIO.cleanup()