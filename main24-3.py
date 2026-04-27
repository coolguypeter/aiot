# ==============================
# AIoT 설계입문 실험
# OpenWeatherMap API를 활용한 온습도 표시 GUI 프로그램
# main24-3.py
# ==============================

# urllib.request:
# 웹 API 서버에 요청을 보내고 응답 데이터를 받아오기 위한 라이브러리
import urllib.request

# json:
# OpenWeatherMap API에서 받은 JSON 형식의 데이터를
# Python 딕셔너리 형태로 변환하기 위한 라이브러리
import json

# tkinter:
# Python에서 GUI 창을 만들기 위한 기본 라이브러리
import tkinter

# tkinter.font:
# GUI 창에 표시되는 글자의 크기와 글꼴을 설정하기 위한 라이브러리
import tkinter.font


# ==============================
# 1. OpenWeatherMap API Key 입력 부분
# ==============================

# OpenWeatherMap 홈페이지에서 발급받은 개인 API Key를 입력한다.
# 주의: 실제 보고서나 제출 자료에는 API Key를 그대로 공개하지 않는 것이 좋다.
API_KEY = "여기에_본인_API_KEY_입력"


# ==============================
# 2. 날씨를 가져올 지역 설정
# ==============================

# 실험한 장소의 지역명을 입력한다.
# 예시:
# 한신대학교 오산캠퍼스 근처라면 "Osan,KR"
# 수원이라면 "Suwon,KR"
# 서울이라면 "Seoul,KR"
CITY = "Osan,KR"


# ==============================
# 3. 날씨 정보를 가져와 GUI에 표시하는 함수
# ==============================

def tick1Min():
    # OpenWeatherMap 현재 날씨 API 요청 URL 생성
    # q       : 날씨를 조회할 도시 이름
    # appid   : 발급받은 API Key
    # units=metric : 온도를 섭씨(°C) 단위로 받기 위한 설정
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    try:
        # urllib.request.urlopen(url):
        # 위에서 만든 URL로 OpenWeatherMap 서버에 요청을 보낸다.
        # 서버는 현재 날씨 정보를 JSON 형식으로 응답한다.
        with urllib.request.urlopen(url) as response:
            # response.read():
            # 서버로부터 받은 응답 데이터를 읽어온다.
            read_data = response.read()

            # json.loads():
            # JSON 형식의 문자열 데이터를 Python 딕셔너리 형태로 변환한다.
            data = json.loads(read_data)

            # OpenWeatherMap 응답 데이터 구조에서
            # main 안에 있는 temp 값을 가져온다.
            # temp는 현재 온도를 의미한다.
            temp = data["main"]["temp"]

            # main 안에 있는 humidity 값을 가져온다.
            # humidity는 현재 습도를 의미한다.
            humi = data["main"]["humidity"]

            # label.config():
            # GUI 화면에 표시되는 텍스트를 변경한다.
            # 온도는 °C, 습도는 % 단위로 표시한다.
            label.config(text=f"{temp:.1f}C   {humi}%")

    except Exception as e:
        # API Key가 아직 활성화되지 않았거나,
        # 인터넷 연결이 안 되었거나,
        # 도시 이름이 잘못되었을 경우 오류가 발생할 수 있다.
        # 오류가 발생하면 GUI 창에 안내 문구를 표시한다.
        label.config(text="데이터 불러오기 실패")

        # 오류 원인을 터미널에서 확인할 수 있도록 출력한다.
        print("오류 발생:", e)

    # window.after(60000, tick1Min):
    # 60000ms = 60초
    # 즉, 60초마다 tick1Min 함수를 다시 실행하여
    # 최신 온도와 습도 정보를 갱신한다.
    window.after(60000, tick1Min)


# ==============================
# 4. GUI 창 생성 및 설정
# ==============================

# tkinter.Tk():
# GUI 프로그램의 기본 창을 생성한다.
window = tkinter.Tk()

# 창 제목 설정
window.title("TEMP HUMI DISPLAY")

# 창 크기 설정
# 400x100은 가로 400px, 세로 100px을 의미한다.
window.geometry("400x100")

# 창 크기 조절 비활성화
# 사용자가 창 크기를 임의로 늘리거나 줄이지 못하게 설정한다.
window.resizable(False, False)

# GUI에 표시될 글자 크기 설정
font = tkinter.font.Font(size=30)

# Label:
# GUI 창 안에 텍스트를 표시하는 위젯이다.
# 처음에는 빈 문자열로 시작하고,
# API 요청 후 온도와 습도 값으로 변경된다.
label = tkinter.Label(window, text="", font=font)

# pack():
# label 위젯을 GUI 창에 배치한다.
label.pack()


# ==============================
# 5. 프로그램 실행
# ==============================

# 프로그램 시작과 동시에 날씨 정보를 한 번 가져온다.
tick1Min()

# mainloop():
# GUI 창이 바로 꺼지지 않고 계속 유지되도록 하는 이벤트 루프이다.
window.mainloop()