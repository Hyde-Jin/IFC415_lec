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

# 호출한 음 출력
def play_ThatsHilarious():
    # 계이름
    Thats_scale = [
        ('디', 0.2), ('리', 0.3), ('피', 0.3), ('리', 0.3), ('시', 0.3), ('피', 0.3), ('리', 0.3), ('시', 0.3), ('피', 0.3), ('피', 0.3), ('피', 0.3),
        ('리', 0.3), ('시', 0.3), ('피', 0.3), ('리', 0.3), ('디', 0.3), ('디', 0.3), ('피', 0.3), ('티', 0.3), ('리', 0.5), ('시', 0.2), ('피', 0.6),
        ('디', 0.3), ('시', 0.3), ('피', 0.5), ('파', 0.2), ('리', 0.6),
        ('리', 0.3), ('리', 0.3), ('리', 0.3), ('시', 0.3), ('피', 0.3), ('리', 0.3), ('시', 0.3), ('피', 0.3), ('피', 0.3), ('피', 0.3),
        ('리', 0.3), ('시', 0.3), ('피', 0.3), ('리', 0.3), ('디', 0.3), ('디', 0.3), ('피', 0.3), ('티', 0.3), ('리', 0.5), ('시', 0.2), ('피', 0.6),
        ('디', 0.3), ('시', 0.3), ('피', 0.5), ('파', 0.2), ('리', 0.6)
    ]

    # 첫 음 재생 전에 바로 주파수를 설정하고 잠깐 대기
    first_note, first_duration = Thats_scale[0]
    p.ChangeFrequency(notes_dict[first_note])
    p.ChangeDutyCycle(1)
    time.sleep(0.1)  # 첫 음이 건너뛰지 않도록 짧은 대기 시간 추가

    # 나머지 음 재생
    for note, duration in Thats_scale:
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