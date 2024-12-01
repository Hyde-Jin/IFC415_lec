import RPi.GPIO as GPIO
import time

# 핀 번호 설정
BUZZER = 12

# 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

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

# 호출한 음 출력
def play_ThatsHilarious():
    # 계이름
    Thats_scale = [
        ('Di', 0.2), ('Ri', 0.3), ('Fi', 0.3), ('Li', 0.3), ('Si', 0.3), ('Fi', 0.3), ('Li', 0.3), ('Si', 0.3), ('Fi', 0.3), ('Fi', 0.3), ('Fi', 0.3),
        ('Li', 0.3), ('Si', 0.3), ('Fi', 0.3), ('Si', 0.3), ('Di', 0.3), ('Di', 0.3), ('Fi', 0.3), ('Ti', 0.3), ('Li', 0.5), ('Si', 0.2), ('Fi', 1.1),
        ('Di', 0.3), ('Si', 0.3), ('Fi', 0.5), ('Fa', 0.2), ('Ri', 1.1),
        ('Fi', 0.3), ('Fi', 0.3), ('Li', 0.3), ('Si', 0.3), ('Fi', 0.3), ('Li', 0.3), ('Si', 0.3), ('Fi', 0.3), ('Fi', 0.3), ('Fi', 0.3),
        ('Li', 0.3), ('Si', 0.3), ('Fi', 0.3), ('Si', 0.3), ('Di', 0.3), ('Di', 0.3), ('Fi', 0.3), ('Ti', 0.3), ('Li', 0.5), ('Si', 0.2), ('Fi', 1.1),
        ('Di', 0.3), ('Si', 0.3), ('Fi', 0.5), ('Fa', 0.2), ('Ri', 1.1)
    ]

    # 첫 음 재생 전에 바로 주파수를 설정하고 잠깐 대기
    first_note, first_duration = Thats_scale[0]
    p.ChangeFrequency(notes_dict[first_note])
    p.ChangeDutyCycle(1)
    time.sleep(0.1)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 나머지 음 재생
    for note, duration in Thats_scale[1:]:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(duration)
    
    # 연주 종료(재시작 대기)
    p.ChangeDutyCycle(0)

try:
    p = GPIO.PWM(BUZZER, 1)
    p.start(0)
    
    play_ThatsHilarious()
    time.sleep(0.2)
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()