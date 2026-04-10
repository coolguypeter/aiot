from gpiozero import MotionSensor      # gpiozero 라이브러리에서 MotionSensor 클래스를 가져옴
import time                            # time 라이브러리를 가져옴

pirPin = MotionSensor(16)              # GPIO 16번 핀을 PIR 모션 센서 입력 핀으로 초기화

try:

    while True:                        # 무한 루프 시작
        sensorValue = pirPin.value     # PIR 센서의 현재 값을 읽어 변수에 저장 (감지:1 / 미감지:0)
        print(sensorValue)             # 센서 값을 터미널에 출력
        time.sleep(0.1)                # 0.1초마다 센서 값을 반복 확인

except KeyboardInterrupt:              # 키보드 인터럽트(Ctrl+C) 발생 시 루프 종료
    pass