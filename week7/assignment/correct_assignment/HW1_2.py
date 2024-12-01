import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5

# 스위치 리스트
switches = [SW1]

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        for i in range(len(switches)):
            current_state = GPIO.input(switches[i])
            if current_state:
                print(f"You clicked switch{i + 1}")
            else:
                print(current_state)

        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()