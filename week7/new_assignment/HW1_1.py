import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        sw1Value = GPIO.input(SW1)
        if sw1Value == 1:
            print("click")
        else:
            print(sw1Value)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()