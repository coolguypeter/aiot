# gpiozero 라이브러리에서 LED 클래스를 가져온다.
# LED 클래스는 라즈베리파이의 GPIO 핀에 연결된 LED를 제어할 때 사용한다.
from gpiozero import LED

# time 라이브러리에서 sleep 함수를 가져온다.
# sleep(초) 형태로 사용하며, 지정한 시간만큼 프로그램을 잠시 멈춘다.
from time import sleep


# -------------------------------
# LED가 연결된 GPIO 핀 번호 설정
# -------------------------------

# 자동차 신호등의 빨간불 LED가 연결된 GPIO 핀 번호
carLedRed = 2

# 자동차 신호등의 노란불 LED가 연결된 GPIO 핀 번호
carLedYellow = 3

# 자동차 신호등의 초록불 LED가 연결된 GPIO 핀 번호
carLedGreen = 4

# 보행자 신호등의 빨간불 LED가 연결된 GPIO 핀 번호
humanLedRed = 20

# 보행자 신호등의 초록불 LED가 연결된 GPIO 핀 번호
humanLedGreen = 21


# -----------------------------------------
# 각 핀 번호를 실제 LED 객체로 다시 초기화
# -----------------------------------------
# 여기서부터는 단순 숫자가 아니라, LED를 제어할 수 있는 객체가 된다.

# GPIO 2번 핀에 연결된 자동차 빨간불 LED 객체 생성
carLedRed = LED(2)

# GPIO 3번 핀에 연결된 자동차 노란불 LED 객체 생성
carLedYellow = LED(3)

# GPIO 4번 핀에 연결된 자동차 초록불 LED 객체 생성
carLedGreen = LED(4)

# GPIO 20번 핀에 연결된 보행자 빨간불 LED 객체 생성
humanLedRed = LED(20)

# GPIO 21번 핀에 연결된 보행자 초록불 LED 객체 생성
humanLedGreen = LED(21)


# 예외가 발생할 수 있는 구간을 try로 감싼다.
# 보통 뒤에 except 또는 finally와 함께 사용한다.
try:
    # 무한 반복문
    # 신호등 동작을 계속 반복하기 위해 while 1을 사용한다.
    while 1:
        # -------------------------------
        # 1단계: 자동차 초록불 / 보행자 빨간불
        # -------------------------------

        # 자동차 빨간불 끄기
        carLedRed.value = 0

        # 자동차 노란불 끄기
        carLedYellow.value = 0

        # 자동차 초록불 켜기
        carLedGreen.value = 1

        # 보행자 빨간불 켜기
        humanLedRed.value = 1

        # 보행자 초록불 끄기
        humanLedGreen.value = 0

        # 현재 상태를 3초 동안 유지
        sleep(3.0)

        # -------------------------------
        # 2단계: 자동차 노란불 / 보행자 빨간불
        # -------------------------------

        # 자동차 빨간불 끄기
        carLedRed.value = 0

        # 자동차 노란불 켜기
        carLedYellow.value = 1

        # 자동차 초록불 끄기
        carLedGreen.value = 0

        # 보행자 빨간불 켜기
        humanLedRed.value = 1

        # 보행자 초록불 끄기
        humanLedGreen.value = 0

        # 현재 상태를 1초 동안 유지
        sleep(1.0)

        # -------------------------------
        # 3단계 시작
        # -------------------------------

        # 자동차 빨간불 켜기
        carLedRed.value = 1