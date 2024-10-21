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

# 버튼 클릭 상태
prev_sw1 = False
prev_sw2 = False
prev_sw3 = False
prev_sw4 = False

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

# 1번 버튼 클릭 시 재생할 노래 (Yuuri - Leo)
def play_Leo():
    # 계이름
    leo_scale = [
        ('도', 0.3), ('파', 0.3), ('미', 0.3), ('파', 0.3), ('솔', 0.3), ('솔', 0.6),
        ('도', 0.3), ('도', 0.3), ('솔', 0.3), ('파', 0.3), ('솔', 0.3), ('라', 0.3), ('라', 0.6),
        ('라', 0.3), ('솔', 0.3), ('파', 0.3), ('미', 0.3), ('파', 0.3), ('라', 0.3), ('라', 0.3), ('솔', 0.3),
        ('레', 0.3), ('미', 0.3), ('파', 0.3), ('미', 0.3), ('미', 0.3), ('파', 0.3), ('파', 0.3)
        ]
    p.ChangeDutyCycle(30)

    # 연주 시작
    for note, duration in leo_scale:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)
    
    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

# 2번 버튼 클릭 시 재생할 노래 (Imase - Night Dancer)
def play_NightDancer():
    # 계이름
    night_scale = [
        ('2솔', 0.4), ('2솔', 0.3), ('2피', 0.3), ('2피', 0.4), ('2레', 0.3), ('2도', 0.3), ('리', 0.3),
        ('2도', 0.3), ('리', 0.3), ('2도', 0.3), ('리', 0.3), ('2레', 0.5),
        ('2도', 0.4), ('2도', 0.3), ('리', 0.3), ('2도', 0.3), ('2레', 0.3),
        ('2파', 0.3), ('2레', 0.3), ('2도', 0.3), ('리', 0.3), ('2도', 0.3), ('2레', 0.3), ('2레', 0.2), ('2도', 0.2)]
    p.ChangeDutyCycle(30)

    # 첫 음 스타카토
    p.ChangeFrequency(notes_dict[night_scale[0][0]])
    time.sleep(0.1)
    p.ChangeDutyCycle(0)
    time.sleep(0.4)
    p.ChangeDutyCycle(30)

    # 연주
    for note, duration in night_scale[1:11]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)
    
    # 쉼표
    p.ChangeFrequency(notes_dict[night_scale[11][0]])
    time.sleep(0.4)
    p.ChangeDutyCycle(0)
    time.sleep(0.3)
    p.ChangeDutyCycle(30)

    # 연주
    for note, duration in night_scale[12:]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)

    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

# 3번 버튼 클릭 시 재생할 노래 (Yuuri - Betelgeuse)
def play_Betelgeuse():
    # 계이름
    bet_scale = [
        ('도', 0.4), ('라', 0.2), ('솔', 0.3), ('파', 0.2), ('파', 0.3), ('2도', 0.2), ('라', 0.3), ('솔', 0.4),
        ('파', 0.2), ('파', 0.3), ('2도', 0.2), ('라', 0.3), ('솔', 0.4),
        ('파', 0.2), ('미', 0.3), ('파', 0.3), ('솔', 0.3), ('파', 0.3)
        ]
    p.ChangeDutyCycle(30)

    # 연주 시작
    for note, duration in bet_scale:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)

    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

# 4번 버튼 클릭 시 재생할 노래 (Yonez Kenshi - Lemon)
def play_Lemon():
    # 계이름
    lemon_scale = [
        ('2디', 0.2), ('2리', 0.15), ('2디', 0.15), ('티', 0.15),
        ('시', 0.2), ('티', 0.5), ('2리', 0.2), ('2피', 0.5), ('2디', 0.2), ('티', 0.5)
        ]
    p.ChangeDutyCycle(30)

    # 첫 음은 빠르게 연주
    for note, duration in lemon_scale:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)
    
    # 한 번 더 반복 연주
    for note, duration in lemon_scale:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)

    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

try:
    p = GPIO.PWM(BUZZER, 1)
    p.start(0)
    while True:
        # None click 상태에서 클릭 시, 버튼별 노래 재생 함수 호출
        if GPIO.input(SW1) and not prev_sw1:
            play_Leo()
        elif GPIO.input(SW2) and not prev_sw2:
            play_NightDancer()
        elif GPIO.input(SW3) and not prev_sw3:
            play_Betelgeuse()
        elif GPIO.input(SW4) and not prev_sw4:
            play_Lemon()
        
        # 버튼 상태 업데이트
        prev_sw1 = GPIO.input(SW1)
        prev_sw2 = GPIO.input(SW2)
        prev_sw3 = GPIO.input(SW3)
        prev_sw4 = GPIO.input(SW4)
        
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()