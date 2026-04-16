# Flask 웹 서버를 만들기 위해 필요한 클래스와 함수들을 가져온다.
# Flask: 웹 애플리케이션 객체를 생성할 때 사용
# render_template: templates 폴더 안의 HTML 파일을 불러와 브라우저 화면에 보여줄 때 사용
# request: 웹페이지에서 사용자가 보낸 데이터(버튼 클릭 값 등)를 서버가 받아올 때 사용
from flask import Flask, render_template, request

# gpiozero 라이브러리의 LED 클래스를 가져온다.
# Raspberry Pi GPIO 핀에 연결된 LED를 켜고 끄기 위해 사용한다.
from gpiozero import LED


# Flask 애플리케이션 객체 생성
# __name__은 현재 실행 중인 파일 이름을 의미하며,
# Flask가 현재 파일을 기준으로 templates 폴더 등을 찾을 수 있게 해준다.
app = Flask(__name__)


# GPIO 21번 핀에 연결된 LED를 제어하기 위한 객체 생성
# LED의 긴 다리(+)를 GPIO 21에 연결하고,
# 짧은 다리(-)는 330Ω 저항을 거쳐 GND에 연결한 상태를 가정한다.
red_led = LED(21)


# 기본 주소('/')로 접속했을 때 실행되는 함수
@app.route('/')
def home():
    # render_template("index.html")의 역할:
    # 1. Flask가 templates 폴더 안에 있는 index.html 파일을 찾는다.
    # 2. 해당 HTML 파일을 읽어서
    # 3. 사용자의 웹 브라우저 화면에 보여준다.
    #
    # 즉, 사용자가 라즈베리파이의 IP 주소로 접속하면
    # 이 함수가 실행되어 LED 제어용 웹페이지가 화면에 나타난다.
    return render_template("index.html")


# '/data' 주소로 POST 요청이 들어왔을 때 실행되는 함수
# HTML form에서 method="post"로 데이터를 보냈기 때문에 POST 방식으로 처리한다.
@app.route('/data', methods=['POST'])
def data():
    # request의 역할:
    # 사용자가 웹페이지에서 버튼을 눌렀을 때,
    # HTML form을 통해 서버로 전달된 데이터를 가져오는 역할을 한다.
    #
    # request.form['led']는
    # <input type="submit" name="led" value="on">
    # <input type="submit" name="led" value="off">
    # 에서 전달된 값을 읽어오는 코드이다.
    #
    # 즉,
    # on 버튼을 누르면 data에는 'on'이 저장되고
    # off 버튼을 누르면 data에는 'off'가 저장된다.
    data = request.form['led']

    # 사용자가 on 버튼을 눌렀을 때
    if data == 'on':
        # GPIO 21번 핀에 연결된 LED를 켠다.
        red_led.on()

    # 사용자가 off 버튼을 눌렀을 때
    elif data == 'off':
        # GPIO 21번 핀에 연결된 LED를 끈다.
        red_led.off()

    # LED 제어가 끝난 뒤 다시 메인 페이지(index.html)를 보여준다.
    # 사용자는 같은 웹페이지에서 계속 on/off 버튼을 누를 수 있다.
    return home()


# 현재 파일을 직접 실행했을 때만 아래 코드가 동작하도록 설정
if __name__ == "__main__":
    # Flask 서버 실행
    #
    # host="0.0.0.0":
    # 라즈베리파이 자신의 로컬 접속만이 아니라
    # 같은 네트워크에 있는 다른 기기에서도 접속할 수 있도록 설정
    #
    # port=80:
    # 웹 기본 포트 80번 사용
    # 80번 포트는 일반적으로 관리자 권한이 필요하므로
    # 터미널에서 sudo python3 main20-1.py 로 실행하는 경우가 많다.
    app.run(host="0.0.0.0", port=80)