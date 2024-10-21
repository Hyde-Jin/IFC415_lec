import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19
PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
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

# 이전 버튼 상태
prev_btn = None

try:
    while True:
        if GPIO.input(SW1):
            if 'sw1' != prev_btn:
                print("You clicked switch1")
                # 현재 버튼 업데이트
                prev_btn = 'sw1'

                # 방향 및 속도 설정 후 출력
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(50)
                R_Motor.ChangeDutyCycle(50)
        elif GPIO.input(SW2):
            if 'sw2' != prev_btn:
                print("You clicked switch2")
                # 현재 버튼 업데이트
                prev_btn = 'sw2'

                # 방향 및 속도 설정 후 출력
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(50)
                R_Motor.ChangeDutyCycle(25)
        elif GPIO.input(SW3):
            if 'sw3' != prev_btn:
                print("You clicked switch3")
                # 현재 버튼 업데이트
                prev_btn = 'sw3'

                # 방향 및 속도 설정 후 출력
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(25)
                R_Motor.ChangeDutyCycle(50)
        elif GPIO.input(SW4):
            if 'sw2' != prev_btn:
                print("You clicked switch4")
                # 현재 버튼 업데이트
                prev_btn = 'sw2'

                # 방향 및 속도 설정 후 출력
                GPIO.output(AIN1, 1)
                GPIO.output(AIN2, 0)
                GPIO.output(BIN1, 1)
                GPIO.output(BIN2, 0)
                L_Motor.ChangeDutyCycle(50)
                R_Motor.ChangeDutyCycle(50)
        else:
            # 만약 버튼을 누르지 않은 상태라면 정지
            if prev_btn is not None:
                L_Motor.ChangeDutyCycle(0)
                R_Motor.ChangeDutyCycle(0)
                prev_btn = None
except KeyboardInterrupt:
    pass

GPIO.cleanup()