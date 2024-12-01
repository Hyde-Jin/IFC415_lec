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
        current_state = GPIO.input(SW1)
        if current_state == 1:
            print("click")
        else:
            print(current_state)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()