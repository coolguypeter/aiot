# main30-1.py
# MQTT 통신으로 제어하는 장치 만들기 - 양방향 통신 실습하기
# 기능:
# 1. PC(MQTT.fx)에서 led 토픽으로 보낸 명령을 Raspberry Pi가 수신함
# 2. 수신한 명령에 따라 초록/파랑/빨강 LED를 켜거나 끔
# 3. 동시에 Raspberry Pi가 hello 토픽으로 1초마다 숫자 데이터를 발행함
# 4. 이를 위해 threading을 사용하여 수신과 발행을 동시에 처리함


import paho.mqtt.client as mqtt   # MQTT 통신을 위한 paho-mqtt 라이브러리 불러오기
import time                       # 1초 대기 등 시간 제어를 위한 time 모듈 불러오기
import threading                  # 송신 작업을 별도 스레드로 실행하기 위한 threading 모듈 불러오기
from gpiozero import LED          # Raspberry Pi GPIO 핀에 연결된 LED를 제어하기 위한 LED 클래스 불러오기


# =========================
# 1. LED GPIO 핀 설정
# =========================

greenLed = LED(16)   # GPIO 16번 핀에 연결된 초록 LED 객체 생성
blueLed = LED(20)    # GPIO 20번 핀에 연결된 파랑 LED 객체 생성
redLed = LED(21)     # GPIO 21번 핀에 연결된 빨강 LED 객체 생성


# =========================
# 2. MQTT 메시지 수신 함수
# =========================

def on_message(client, userdata, msg):
    # PC의 MQTT.fx에서 led 토픽으로 메시지를 보내면 이 함수가 자동으로 실행됨

    print(msg.topic + " " + str(msg.payload))
    # 수신된 토픽 이름과 payload 원본 데이터를 터미널에 출력함
    # msg.topic: 메시지가 들어온 토픽 이름
    # msg.payload: 실제로 전달된 데이터, 바이트 형태로 들어옴

    message = msg.payload.decode("utf-8")
    # MQTT로 받은 payload는 바이트 형태이므로 문자열로 변환함
    # 예: b'green_on' -> 'green_on'

    print("수신 메시지:", message)
    # 변환된 문자열 메시지를 터미널에 출력함

    if message == "green_on":
        # 수신 메시지가 green_on이면 초록 LED 켜기
        greenLed.on()

    elif message == "green_off":
        # 수신 메시지가 green_off이면 초록 LED 끄기
        greenLed.off()

    elif message == "blue_on":
        # 수신 메시지가 blue_on이면 파랑 LED 켜기
        blueLed.on()

    elif message == "blue_off":
        # 수신 메시지가 blue_off이면 파랑 LED 끄기
        blueLed.off()

    elif message == "red_on":
        # 수신 메시지가 red_on이면 빨강 LED 켜기
        redLed.on()

    elif message == "red_off":
        # 수신 메시지가 red_off이면 빨강 LED 끄기
        redLed.off()

    else:
        # 정해진 명령어가 아닌 값이 들어오면 안내 메시지 출력
        print("알 수 없는 명령어입니다:", message)


# =========================
# 3. MQTT 클라이언트 생성 및 연결
# =========================

client = mqtt.Client()
# MQTT 클라이언트 객체 생성
# 이 객체를 통해 Broker 연결, 토픽 구독, 메시지 발행을 수행함

client.on_message = on_message
# 메시지가 수신되었을 때 실행할 함수를 on_message 함수로 지정함

broker_address = "192.168.137.230"
# MQTT Broker 주소 입력
# 실습에서는 보통 Raspberry Pi의 IP 주소를 입력함
# 본인 라즈베리파이 IP가 다르면 이 부분을 수정해야 함

client.connect(broker_address)
# 위에서 설정한 MQTT Broker에 연결함

client.subscribe("led", 1)
# led 토픽을 구독함
# PC의 MQTT.fx에서 led 토픽으로 메시지를 발행하면 Raspberry Pi가 수신함
# 뒤의 1은 QoS 1을 의미하며, 메시지를 최소 1회 수신하도록 보장하는 설정임


# =========================
# 4. hello 토픽 발행용 변수
# =========================

count = 0
# hello 토픽으로 보낼 숫자의 초기값을 0으로 설정함


# =========================
# 5. 숫자 데이터를 발행하는 스레드 함수
# =========================

def send_thread():
    # 이 함수는 별도의 스레드에서 실행됨
    # Raspberry Pi가 1초마다 hello 토픽으로 숫자 데이터를 발행함

    global count
    # 함수 밖에 있는 count 변수를 함수 안에서 수정하기 위해 global로 선언함

    while True:
        # 프로그램이 종료되기 전까지 계속 반복함

        count = count + 1
        # count 값을 1씩 증가시킴

        client.publish("hello", str(count))
        # hello 토픽으로 count 값을 발행함
        # 숫자는 MQTT 메시지로 보내기 위해 문자열로 변환함

        print("발행 메시지: hello", count)
        # 터미널에서 발행되는 값을 확인하기 위해 출력함

        time.sleep(1.0)
        # 1초 동안 대기한 뒤 다시 숫자를 발행함


# =========================
# 6. 스레드 실행
# =========================

task = threading.Thread(target=send_thread)
# send_thread 함수를 실행할 별도의 스레드 객체를 생성함
# 이 스레드는 hello 토픽으로 숫자를 계속 발행하는 역할을 함

task.daemon = True
# 메인 프로그램이 종료될 때 스레드도 함께 종료되도록 설정함

task.start()
# 스레드 시작
# 이 시점부터 hello 토픽 발행 작업이 메인 코드와 동시에 실행됨


# =========================
# 7. MQTT 메시지 수신 대기
# =========================

try:
    # Ctrl + C로 종료할 수 있도록 예외 처리를 사용함

    client.loop_forever()
    # MQTT 메시지를 계속 수신하기 위한 무한 대기 루프
    # led 토픽으로 메시지가 들어오면 on_message 함수가 자동 실행됨
    # 이 함수는 계속 실행되므로, 숫자 발행은 별도 스레드에서 처리해야 함

except KeyboardInterrupt:
    # 사용자가 Ctrl + C를 누르면 프로그램 종료 처리

    print("프로그램을 종료합니다.")

finally:
    # 프로그램이 종료될 때 LED를 모두 끄고 MQTT 연결을 종료함

    greenLed.off()
    # 초록 LED 끄기

    blueLed.off()
    # 파랑 LED 끄기

    redLed.off()
    # 빨강 LED 끄기

    client.disconnect()
    # MQTT Broker와 연결 해제