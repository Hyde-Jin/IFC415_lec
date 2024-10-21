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
scale = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti', '2Do']

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