import RPi.GPIO as GPIO
import time

# 핀 번호 설정
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19
BUZZER = 12

# 스위치 리스트
switches = [SW1, SW2, SW3, SW4]

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
for sw in switches:
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 음별 주파수
notes_dict = {
    'Do': 261.63,
    'Di' : 277.18,
    'Re': 293.66,
    'Ri' : 311.13,
    'Mi': 329.63,
    'Fa': 349.23,
    'Fi' : 369.99,
    'Sol': 392.00,
    'Si' : 415.30,
    'La': 440.00,
    'Li' : 466.16,
    'Ti': 493.88,
    '2Do': 523.25,
    '2Di' : 554.37,
    '2Re' : 587.33,
    '2Ri' : 622.25,
    '2Mi' : 659.25,
    '2Fa' : 698.46,
    '2Fi' : 739.99,
    '2Sol' : 783.99
}

# 과제에서 사용할 음
scale = ['2Di', '2Li', 'Si', '2Fa']

# 현재 음
current_note = None

# 호출한 음 출력
def play_sound(note):
    # 전역 변수값 수정
    global current_note
    
    # 이전 음과 다른 음을 호출했다면
    if note != current_note:
        p.ChangeDutyCycle(1)
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
            play_sound('2Di')
        elif GPIO.input(SW2):
            play_sound('2Ri')
        elif GPIO.input(SW3):
            play_sound('Si')
        elif GPIO.input(SW4):
            play_sound('2Fa')
        else:
            # 만약 버튼을 누르지 않은 상태라면 음소거
            if current_note is not None:
                p.ChangeDutyCycle(0)
                current_note = None
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()