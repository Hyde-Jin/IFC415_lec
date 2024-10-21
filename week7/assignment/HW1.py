import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# 카운트 리스트 (1번 버튼부터 4번 버튼 순서)
cntlist = [0, 0, 0, 0]

# 버튼 클릭 상태
prev_sw1 = False
prev_sw2 = False
prev_sw3 = False
prev_sw4 = False

try:
    print(f"click the switch!")
    while True:
        # None click 상태에서 1번 버튼 클릭 시, 1번 카운트 증가 후 출력
        if GPIO.input(SW1) and not prev_sw1:
            cntlist[0] += 1
            print(f"You clicked Switch1, total number of clicks = {cntlist}")

        # None click 상태에서 2번 버튼 클릭 시, 2번 카운트 증가 후 출력
        if GPIO.input(SW2) and not prev_sw2:
            cntlist[1] += 1
            print(f"You clicked Switch2, total number of clicks = {cntlist}")
        
        # None click 상태에서 3번 버튼 클릭 시, 3번 카운트 증가 후 출력
        if GPIO.input(SW3) and not prev_sw3:
            cntlist[2] += 1
            print(f"You clicked Switch3, total number of clicks = {cntlist}")
        
        # None click 상태에서 4번 버튼 클릭 시, 4번 카운트 증가 후 출력
        if GPIO.input(SW4) and not prev_sw4:
            cntlist[3] += 1
            print(f"You clicked Switch4, total number of clicks = {cntlist}")
        
        # 버튼 상태 업데이트
        prev_sw1 = GPIO.input(SW1)
        prev_sw2 = GPIO.input(SW2)
        prev_sw3 = GPIO.input(SW3)
        prev_sw4 = GPIO.input(SW4)

        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()