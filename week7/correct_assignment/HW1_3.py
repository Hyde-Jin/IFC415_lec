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

# 이전 상태를 저장할 리스트 생성 및 초기화
previous_states = []
for sw in switches:
    previous_states.append(sw)

try:
    while True:
        for i in range(len(switches)):
            current_state = GPIO.input(switches[i])
            if current_state and not previous_states[i]:
                print(f"You clicked switch{i + 1}")
            previous_states[i] = current_state
        
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()