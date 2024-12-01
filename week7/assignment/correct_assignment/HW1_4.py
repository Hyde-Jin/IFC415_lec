import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

# 스위치 리스트
switches = [SW1, SW2, SW3, SW4]

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for sw in switches:
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 카운트 리스트 (1번 버튼부터 4번 버튼 순서)
cntlist = [0, 0, 0, 0]

# 이전 상태를 저장할 리스트 생성 및 초기화
previous_states = []
for sw in switches:
    previous_states.append(sw)

try:
    print(f"click the switch!")
    while True:
        for i in range(len(switches)):
            current_state = GPIO.input(switches[i])
            if current_state and not previous_states[i]:
                cntlist[i] += 1
                print(f"You clicked switch{i + 1}, count = {cntlist}")
            previous_states[i] = current_state

        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()