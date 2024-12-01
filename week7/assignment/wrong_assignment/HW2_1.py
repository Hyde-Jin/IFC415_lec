import RPi.GPIO as GPIO
import time

# 핀번호 설정
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

# 과제에서 사용할 음
scale = ['도', '레', '미', '파', '솔', '라', '시', '2도']

try:
    p = GPIO.PWM(BUZZER, notes_dict[scale[0]])
    p.start(50)
    
    # 음계 리스트에서 하나씩 출력
    for note in scale:
        p.ChangeFrequency(notes_dict[note])
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()