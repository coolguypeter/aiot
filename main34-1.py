# OpenCV 라이브러리를 불러온다.
# OpenCV는 웹캠 영상을 가져오고, 얼굴과 눈을 인식하는 데 사용된다.
import cv2

# gpiozero 라이브러리에서 Buzzer 클래스를 불러온다.
# Buzzer는 Raspberry Pi의 GPIO 핀에 연결된 능동부저를 제어할 때 사용된다.
from gpiozero import Buzzer

# 시간 지연 처리를 위해 time 라이브러리를 불러온다.
# 본 코드에서는 필요 시 짧은 대기 시간을 줄 때 사용할 수 있다.
import time


# GPIO 16번 핀에 연결된 능동부저 객체를 생성한다.
# 이후 buzzerPin.on()을 실행하면 부저 경보음이 울리고,
# buzzerPin.off()를 실행하면 부저 경보음이 멈춘다.
buzzerPin = Buzzer(16)


# 프로그램의 전체 동작을 main 함수 안에 작성한다.
def main():

    # 웹캠을 실행한다.
    # -1은 Raspberry Pi에 연결된 웹캠을 자동으로 선택하라는 의미이다.
    camera = cv2.VideoCapture(-1)

    # 웹캠 영상의 가로 해상도를 640픽셀로 설정한다.
    camera.set(3, 640)

    # 웹캠 영상의 세로 해상도를 480픽셀로 설정한다.
    camera.set(4, 480)

    # OpenCV에 기본으로 포함된 정면 얼굴 인식용 Haar Cascade XML 파일 경로를 가져온다.
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

    # OpenCV에 기본으로 포함된 눈 인식용 Haar Cascade XML 파일 경로를 가져온다.
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'

    # 얼굴을 인식하기 위한 분류기 객체를 생성한다.
    face_cascade = cv2.CascadeClassifier(face_xml)

    # 눈을 인식하기 위한 분류기 객체를 생성한다.
    eye_cascade = cv2.CascadeClassifier(eye_xml)

    # 프로그램 실행 중 오류가 발생하거나 사용자가 종료해도
    # 웹캠과 부저가 안전하게 정리되도록 try-finally 구조를 사용한다.
    try:

        # 웹캠이 정상적으로 열려 있는 동안 계속 반복한다.
        while camera.isOpened():

            # 웹캠에서 현재 프레임을 한 장 읽어온다.
            # ret은 프레임을 정상적으로 읽었는지 여부이고,
            # image는 실제 웹캠 이미지 데이터이다.
            ret, image = camera.read()

            # 웹캠 프레임을 정상적으로 읽지 못했다면 반복문을 종료한다.
            if not ret:
                print("웹캠 영상을 읽을 수 없습니다.")
                break

            # 얼굴과 눈 인식은 컬러 이미지보다 흑백 이미지에서 더 효율적으로 수행된다.
            # 따라서 BGR 컬러 이미지를 흑백 이미지로 변환한다.
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 흑백 이미지에서 얼굴을 탐지한다.
            # scaleFactor=1.1 : 탐지 창의 크기를 10%씩 키워가며 얼굴을 찾는다.
            # minNeighbors=5 : 최소 5번 이상 얼굴로 판단된 영역만 실제 얼굴로 인정한다.
            # minSize=(100, 100) : 너무 작은 영역은 얼굴로 보지 않는다.
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # 현재 프레임에서 감지된 얼굴의 개수를 터미널에 출력한다.
            print("faces detected Number: " + str(len(faces)))

            # 감지된 얼굴이 없을 경우에는 부저 경보음이 울리지 않도록 한다.
            # 얼굴이 없는데 눈도 없다고 판단해서 부저가 울리는 상황을 방지하기 위함이다.
            if len(faces) == 0:
                buzzerPin.off()

            # 감지된 얼굴 영역을 하나씩 처리한다.
            for (x, y, w, h) in faces:

                # 원본 웹캠 화면에서 얼굴 위치에 파란색 사각형을 그린다.
                # (x, y)는 얼굴 영역의 왼쪽 위 좌표이고,
                # (x+w, y+h)는 얼굴 영역의 오른쪽 아래 좌표이다.
                cv2.rectangle(
                    image,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 0),
                    2
                )

                # 전체 흑백 이미지에서 얼굴 영역만 잘라낸다.
                # 눈은 얼굴 내부에서만 탐지하도록 하기 위해 사용한다.
                face_gray = gray[y:y + h, x:x + w]

                # 전체 컬러 이미지에서 얼굴 영역만 잘라낸다.
                # 눈 위치에 초록색 사각형을 표시하기 위해 사용한다.
                face_color = image[y:y + h, x:x + w]

                # 얼굴 영역 안에서 눈을 탐지한다.
                # 눈은 얼굴 내부에서만 찾기 때문에 전체 화면에서 찾는 것보다 효율적이다.
                eyes = eye_cascade.detectMultiScale(
                    face_gray,
                    scaleFactor=1.1,
                    minNeighbors=5
                )

                # 현재 얼굴 영역에서 감지된 눈의 개수를 터미널에 출력한다.
                print("eyes detected Number: " + str(len(eyes)))

                # 감지된 눈의 개수가 1개 이하이면 눈을 감은 상태로 판단한다.
                # 본 실험에서는 눈을 깜빡여 눈이 감기는 순간,
                # 감지되는 눈의 개수가 줄어들면 부저 경보음이 울리는지 확인하였다.
                if len(eyes) <= 1:
                    print("눈 감김 감지 - 부저 경보음 발생")
                    buzzerPin.on()

                # 감지된 눈의 개수가 2개 이상이면 정상 상태로 판단한다.
                # 이 경우에는 부저 경보음이 울리지 않도록 한다.
                else:
                    print("정상 상태 - 부저 경보음 없음")
                    buzzerPin.off()

                # 감지된 눈 영역을 하나씩 처리한다.
                for (ex, ey, ew, eh) in eyes:

                    # 얼굴 영역 안에서 눈 위치에 초록색 사각형을 그린다.
                    # 이를 통해 웹캠 화면에서 눈이 정상적으로 인식되는지 확인할 수 있다.
                    cv2.rectangle(
                        face_color,
                        (ex, ey),
                        (ex + ew, ey + eh),
                        (0, 255, 0),
                        2
                    )

            # 얼굴과 눈 인식 결과가 표시된 화면을 GUI 창에 출력한다.
            cv2.imshow('result', image)

            # 키보드 입력을 1ms 동안 기다린다.
            # 사용자가 q 키를 누르면 프로그램을 종료한다.
            if cv2.waitKey(1) == ord('q'):
                break

    # 프로그램이 종료될 때 반드시 실행되는 부분이다.
    finally:

        # 프로그램 종료 시 부저 경보음이 계속 울리지 않도록 멈춘다.
        buzzerPin.off()

        # 사용 중이던 웹캠 자원을 해제한다.
        camera.release()

        # OpenCV로 열린 모든 창을 닫는다.
        cv2.destroyAllWindows()


# 이 파일을 직접 실행했을 때만 main 함수가 실행되도록 한다.
if __name__ == '__main__':
    main()