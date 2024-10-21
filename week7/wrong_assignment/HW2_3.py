import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19
BUZZER = 12

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUZZER, GPIO.OUT)

# 음별 주파수
notes_dict = {
    '도': 261.63,
    '디' : 277.18,
    '레': 293.66,
    '리' : 311.13,
    '미': 329.63,
    '파': 349.23,
    '피' : 369.99,
    '솔': 392.00,
    '시' : 415.30,
    '라': 440.00,
    '리' : 466.16,
    '티': 493.88,
    '2도': 523.25,
    '2디' : 554.37,
    '2레' : 587.33,
    '2리' : 622.25,
    '2미' : 659.25,
    '2파' : 698.46,
    '2피' : 739.99,
    '2솔' : 783.99
}

# 과제에서 사용할 음
scale = ['2디', '2리', '시', '2파']

# 현재 음
current_note = None

# 호출한 음 출력
def play_sound(note):
    # 전역 변수값 수정
    global current_note
    
    # 이전 음과 다른 음을 호출했다면
    if note != current_note:
        p.ChangeDutyCycle(30)
        # 현재 음 업데이트
        current_note = note
        # 현재 음 출력
        p.ChangeFrequency(notes_dict[current_note])

try:
    p = GPIO.PWM(BUZZER, 1)
    p.start(0)
    while True:
        # 버튼별 특정 음 재생을 위해 함수 호출
        if GPIO.input(SW1):
            play_sound('2디')
        elif GPIO.input(SW2):
            play_sound('2리')
        elif GPIO.input(SW3):
            play_sound('시')
        elif GPIO.input(SW4):
            play_sound('2파')
        else:
            # 만약 버튼을 누르지 않은 상태라면 음소거
            if current_note is not None:
                p.ChangeDutyCycle(0)
                current_note = None
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()