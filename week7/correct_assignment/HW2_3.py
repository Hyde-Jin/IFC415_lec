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
for sw in switches:
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 버튼 클릭 상태
prev_sw1 = False
prev_sw2 = False
prev_sw3 = False
prev_sw4 = False

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
    '2Sol' : 783.99,
    '2Si' : 830.61,
    '2La' : 880.00,
    '2Li' : 932.33,
    '2Ti' : 987.77
}

# 1번 버튼 클릭 시 재생할 노래 (Yuuri - Leo)
def play_Leo():
    # 계이름
    leo_scale = [
        ('Do', 0.3), ('Fa', 0.3), ('Mi', 0.3), ('Fa', 0.3), ('Sol', 0.3), ('Sol', 0.6),
        ('Do', 0.3), ('Do', 0.3), ('Sol', 0.3), ('Fa', 0.3), ('Sol', 0.3), ('La', 0.3), ('La', 0.6),
        ('La', 0.3), ('Sol', 0.3), ('Fa', 0.3), ('Mi', 0.3), ('Fa', 0.3), ('La', 0.3), ('La', 0.3), ('Sol', 0.3),
        ('Re', 0.3), ('Mi', 0.3), ('Fa', 0.3), ('Mi', 0.3), ('Mi', 0.3), ('Fa', 0.3), ('Fa', 0.3)
        ]

    # 첫 음 재생 전에 바로 주파수를 설정하고 잠깐 대기
    first_note, first_dulation = leo_scale[0]
    p.ChangeFrequency(notes_dict[first_note])
    p.ChangeDutyCycle(1)
    time.sleep(0.2)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 연주 시작
    for note, dulation in leo_scale[1:]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(dulation)
    
    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

# 2번 버튼 클릭 시 재생할 노래 (Imase - Night Dancer)
def play_NightDancer():
    # 계이름
    night_scale = [
        ('2Sol', 0.4), ('2Sol', 0.25), ('2Fi', 0.25), ('2Fi', 0.35), ('2Re', 0.25), ('2Do', 0.25), ('Li', 0.25),
        ('2Do', 0.25), ('Li', 0.25), ('2Do', 0.25), ('Li', 0.25), ('2Re', 0.5),
        ('2Do', 0.35), ('2Do', 0.25), ('Li', 0.25), ('2Do', 0.25), ('2Re', 0.25),
        ('2Fa', 0.25), ('2Re', 0.25), ('2Do', 0.25), ('Li', 0.25), ('2Do', 0.25), ('2Re', 0.25), ('2Re', 0.4)
        ]
    
    # 첫 음 재생 전에 바로 주파수를 설정하고 잠깐 대기
    first_note, first_dulation = night_scale[0]
    p.ChangeFrequency(notes_dict[first_note])
    p.ChangeDutyCycle(1)
    time.sleep(0.15)
    p.ChangeDutyCycle(0)
    time.sleep(0.3)
    p.ChangeDutyCycle(1)
    time.sleep(0.1)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 연주
    for note, dulation in night_scale[1:11]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(dulation)
    
    # 쉼표
    p.ChangeFrequency(notes_dict[night_scale[11][0]])
    time.sleep(0.3)
    p.ChangeDutyCycle(0)
    time.sleep(0.3)
    p.ChangeDutyCycle(1)
    time.sleep(0.2)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 연주
    for note, dulation in night_scale[12:]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(dulation)

    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

# 3번 버튼 클릭 시 재생할 노래 (Yuuri - Betelgeuse)
def play_Betelgeuse():
    # 계이름
    bet_scale = [
        ('Do', 0.3), ('La', 0.2), ('Sol', 0.3), ('Fa', 0.2),
        ('Fa', 0.3), ('2Do', 0.2), ('La', 0.3), ('Sol', 0.4), ('Fa', 0.2), ('Fa', 0.3), ('2Do', 0.2), ('La', 0.3), ('Sol', 0.4), ('Fa', 0.2),
        ('Mi', 0.3), ('Fa', 0.3), ('Sol', 0.3), ('Fa', 0.7), 
        ('Do', 0.3), ('Mi', 0.3), ('Fa', 0.3), ('Fa', 0.3), ('2Do', 0.2), ('La', 0.3), ('Sol', 0.4),
        ('Fa', 0.2), ('Fa', 0.3), ('2Do', 0.2), ('La', 0.3), ('Sol', 0.4),
        ('Fa', 0.2), ('Li', 0.3), ('La', 0.3), ('Sol', 0.3), ('Mi', 0.3), ('Fa', 0.3)
        ]
    
    # 첫 음 재생 전에 바로 주파수를 설정하고 잠깐 대기
    first_note, first_dulation = bet_scale[0]
    p.ChangeFrequency(notes_dict[first_note])
    p.ChangeDutyCycle(1)
    time.sleep(0.2)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 연주 시작
    for note, dulation in bet_scale[1:]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(dulation)

    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

# 4번 버튼 클릭 시 재생할 노래 (Yonez Kenshi - Lemon)
def play_Lemon():
    # 계이름
    lemon_scale = [
        ('2Di', 0.2), ('2Ri', 0.15), ('2Di', 0.15), ('Ti', 0.15), ('Si', 0.2), ('Ti', 0.5), ('2Ri', 0.2), ('2Fi', 0.5), ('2Di', 0.2), ('Ti', 0.5),
        ('2Di', 0.2), ('2Ri', 0.15), ('2Di', 0.15), ('Ti', 0.15), ('Si', 0.2), ('Ti', 0.5), ('2Ri', 0.2), ('2Fi', 0.5), ('2Di', 0.2), ('Ti', 0.5),
        ('2Di', 0.2), ('2Ri', 0.15), ('2Di', 0.15), ('Ti', 0.15), ('Si', 0.2), ('Ti', 0.5), ('2Ri', 0.2), ('2Fi', 0.5),
        ('2Si', 0.2), ('2Fi', 0.5), ('2Fi', 0.2), ('2Ti', 0.5), ('2Li', 0.2), ('2Fi', 0.5), ('2Ri', 0.2), ('2Fi', 0.5), ('2Di', 1.0)
        ]
    
    # 첫 음 재생 전에 바로 주파수를 설정하고 잠깐 대기
    first_note, first_dulation = lemon_scale[0]
    p.ChangeFrequency(notes_dict[first_note])
    p.ChangeDutyCycle(1)
    time.sleep(0.2)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 연주 시작
    for note, dulation in lemon_scale[1:]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(dulation)

    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

try:
    p = GPIO.PWM(BUZZER, 1)
    p.start(0)
    p.ChangeDutyCycle(0)

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