# ==============================
# AIoT 기말 프로젝트 최종 코드
# OpenCV DNN 객체 인식 + 사람 감지 + 텔레그램 알림
# ==============================

# OpenCV 라이브러리 불러오기
# 카메라 영상 입력, 이미지 처리, 객체 인식 결과 표시 등에 사용
import cv2

# 시간 관련 기능을 사용하기 위한 라이브러리
# 알림 중복 전송 방지 시간 계산에 사용
import time

# 텔레그램 API 요청을 보내기 위한 라이브러리
# 별도 requests 설치 없이 파이썬 기본 기능으로 메시지 전송 가능
import urllib.request
import urllib.parse


# ==============================
# 1. 텔레그램 설정
# ==============================

# 텔레그램 봇 토큰
# BotFather를 통해 발급받은 토큰을 입력
TELEGRAM_TOKEN = "텔레그램_BOT_TOKEN_입력"

# 텔레그램 사용자 ID
# 알림 메시지를 받을 사용자의 chat_id 입력
TELEGRAM_CHAT_ID = "TELEGRAM_ID_입력"

# 알림 메시지 전송 간격 설정
# 사람이 계속 감지될 때 메시지가 계속 전송되는 것을 막기 위함
# 예: 10초에 한 번만 알림 전송
ALERT_INTERVAL = 10

# 마지막으로 텔레그램 알림을 보낸 시간을 저장하는 변수
# 처음에는 알림을 보낸 적이 없으므로 0으로 설정
last_alert_time = 0


# ==============================
# 2. 텔레그램 메시지 전송 함수
# ==============================

def send_telegram_message(message):
    """
    텔레그램으로 알림 메시지를 전송하는 함수
    사람이 감지되었을 때 이 함수를 호출하여 사용자에게 알림을 보냄
    """

    try:
        # 텔레그램 Bot API 주소 생성
        # sendMessage 기능을 사용하여 특정 chat_id로 메시지를 전송
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        # 텔레그램 API에 전달할 데이터 구성
        data = {
            "chat_id": TELEGRAM_CHAT_ID,   # 메시지를 받을 사용자 ID
            "text": message                # 실제로 보낼 메시지 내용
        }

        # 한글 메시지도 정상적으로 전송되도록 URL 인코딩 처리
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")

        # 텔레그램 서버로 메시지 전송 요청
        urllib.request.urlopen(url, encoded_data)

        # 터미널에 메시지 전송 성공 여부 출력
        print("[Telegram] 알림 메시지 전송 완료:", message)

    except Exception as e:
        # 텔레그램 전송 중 오류가 발생하면 오류 내용 출력
        print("[Telegram] 메시지 전송 실패:", e)


# ==============================
# 3. 객체 인식 모델 설정
# ==============================

# MobileNetSSD 모델이 구분할 수 있는 객체 목록
# 숫자 ID에 따라 객체 이름이 정해져 있음
classNames = {
    0: 'background',
    1: 'aeroplane',
    2: 'bicycle',
    3: 'bird',
    4: 'boat',
    5: 'bottle',
    6: 'bus',
    7: 'car',
    8: 'cat',
    9: 'chair',
    10: 'cow',
    11: 'diningtable',
    12: 'dog',
    13: 'horse',
    14: 'motorbike',
    15: 'person',
    16: 'pottedplant',
    17: 'sheep',
    18: 'sofa',
    19: 'train',
    20: 'tvmonitor'
}

# 객체 인식 모델 구조 파일
# MobileNetSSD의 네트워크 구조가 저장된 파일
prototxt_path = "MobileNetSSD_deploy.prototxt.txt"

# 객체 인식 모델 가중치 파일
# 학습된 모델 데이터가 저장된 파일
model_path = "MobileNetSSD_deploy.caffemodel"

# OpenCV DNN 모듈을 이용하여 모델 불러오기
# prototxt 파일과 caffemodel 파일을 함께 사용해야 함
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)


# ==============================
# 4. 카메라 설정
# ==============================

# 웹캠 연결
# 0번은 기본 카메라를 의미함
# 라즈베리파이에서 카메라가 여러 개면 1 또는 2로 바꿔야 할 수도 있음
cap = cv2.VideoCapture(0)

# 카메라가 정상적으로 열리지 않았을 때 오류 메시지 출력
if not cap.isOpened():
    print("카메라를 열 수 없습니다. 웹캠 연결 상태를 확인하세요.")
    exit()

# 카메라 화면 가로 크기 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

# 카메라 화면 세로 크기 설정
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# ==============================
# 5. 실시간 객체 인식 실행
# ==============================

print("AIoT 침입 감지 시스템 실행 중...")
print("사람이 감지되면 텔레그램 알림이 전송됩니다.")
print("종료하려면 키보드에서 q를 누르세요.")


while True:
    # 카메라에서 한 프레임씩 영상 읽기
    # ret은 영상 읽기 성공 여부, frame은 실제 이미지 데이터
    ret, frame = cap.read()

    # 프레임을 정상적으로 읽지 못한 경우 반복문 종료
    if not ret:
        print("카메라 영상을 읽을 수 없습니다.")
        break

    # 현재 프레임의 높이와 너비 가져오기
    h, w = frame.shape[:2]

    # DNN 모델에 입력하기 위한 이미지 전처리
    # blobFromImage는 이미지를 모델 입력 형식으로 변환하는 함수
    blob = cv2.dnn.blobFromImage(
        frame,                  # 입력 이미지
        scalefactor=0.007843,   # 픽셀 값 정규화 비율
        size=(300, 300),        # 모델 입력 크기
        mean=127.5              # 평균값 보정
    )

    # 전처리한 이미지를 객체 인식 모델에 입력
    net.setInput(blob)

    # 객체 인식 실행
    # detections에는 감지된 객체 정보가 저장됨
    detections = net.forward()

    # 현재 프레임에서 사람이 감지되었는지 확인하기 위한 변수
    person_detected = False

    # 감지된 객체 개수만큼 반복
    for i in range(detections.shape[2]):

        # 객체 인식 신뢰도 값 가져오기
        # confidence가 높을수록 모델이 해당 객체라고 확신하는 정도가 높음
        confidence = detections[0, 0, i, 2]

        # 신뢰도가 0.5 이상인 경우에만 객체로 인정
        # 너무 낮은 신뢰도는 오탐지 가능성이 높기 때문
        if confidence > 0.5:

            # 감지된 객체의 클래스 ID 가져오기
            class_id = int(detections[0, 0, i, 1])

            # 클래스 ID를 객체 이름으로 변환
            object_name = classNames.get(class_id, "unknown")

            # 감지된 객체의 위치 좌표 계산
            box = detections[0, 0, i, 3:7] * [w, h, w, h]

            # 좌표를 정수형으로 변환
            startX, startY, endX, endY = box.astype("int")

            # 감지된 객체 주변에 사각형 표시
            cv2.rectangle(
                frame,
                (startX, startY),
                (endX, endY),
                (0, 255, 0),
                2
            )

            # 화면에 표시할 객체 이름과 신뢰도 텍스트 생성
            label = f"{object_name}: {confidence * 100:.2f}%"

            # 객체 이름과 신뢰도를 화면에 출력
            cv2.putText(
                frame,
                label,
                (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # 감지된 객체가 사람인 경우
            if object_name == "person":

                # 사람 감지 여부를 True로 변경
                person_detected = True

                # 터미널에 사람 감지 메시지 출력
                print("사람 감지됨!")


    # ==============================
    # 6. 사람 감지 시 텔레그램 알림 전송
    # ==============================

    # 현재 시간 가져오기
    current_time = time.time()

    # 사람이 감지되었고, 마지막 알림 이후 ALERT_INTERVAL초 이상 지났다면 알림 전송
    if person_detected and current_time - last_alert_time > ALERT_INTERVAL:

        # 텔레그램으로 보낼 메시지 내용
        alert_message = "사람이 침입했습니다."

        # 텔레그램 메시지 전송 함수 호출
        send_telegram_message(alert_message)

        # 마지막 알림 시간을 현재 시간으로 갱신
        last_alert_time = current_time


    # ==============================
    # 7. 화면 출력 및 종료 처리
    # ==============================

    # 객체 인식 결과가 표시된 영상을 화면에 출력
    cv2.imshow("AIoT Intrusion Detection System", frame)

    # 키보드 입력을 1ms 동안 기다림
    key = cv2.waitKey(1) & 0xFF

    # 사용자가 q 키를 누르면 프로그램 종료
    if key == ord('q'):
        print("프로그램을 종료합니다.")
        break


# ==============================
# 8. 자원 정리
# ==============================

# 카메라 사용 종료
cap.release()

# OpenCV로 생성한 모든 창 닫기
cv2.destroyAllWindows()

# 프로그램 종료 메시지 출력
print("AIoT 침입 감지 시스템 종료")