# ============================================================
# 파일명: main32-2.py
# 실험명: 인공지능 음성을 인식하여 날씨 정보 알려주는 장치 만들기
# 기능:
#   1. 마이크로 사용자의 음성을 입력받음
#   2. Google Speech Recognition을 이용해 음성을 텍스트로 변환함
#   3. 인식된 텍스트에 "날씨"라는 단어가 있으면 OpenWeatherMap API로 서울 날씨를 요청함
#   4. 받아온 기온과 습도 정보를 한글 문장으로 구성함
#   5. espeak TTS를 이용해 날씨 정보를 음성으로 출력함
# ============================================================


# speech_recognition 라이브러리를 sr이라는 이름으로 불러옴
# 이 라이브러리는 마이크 입력을 받아 음성을 텍스트로 변환할 때 사용함
import speech_recognition as sr

# requests 라이브러리를 불러옴
# OpenWeatherMap API에 HTTP 요청을 보내 날씨 데이터를 받아올 때 사용함
import requests

# subprocess 라이브러리를 불러옴
# 라즈베리파이에서 espeak 명령어를 안전하게 실행하기 위해 사용함
import subprocess

# time 라이브러리를 불러옴
# 반복 실행 중 잠깐 대기 시간을 줄 때 사용함
import time


# ------------------------------------------------------------
# OpenWeatherMap API 키 설정
# ------------------------------------------------------------

# 본인의 OpenWeatherMap API 키를 아래 문자열 안에 입력해야 함
# 예: API_KEY = "abcd1234..."
# 깃허브에 올릴 때는 실제 API 키를 그대로 올리지 않는 것이 좋음
API_KEY = "Enter your API key here"


# ------------------------------------------------------------
# 날씨를 조회할 도시와 API 요청 URL 설정
# ------------------------------------------------------------

# 날씨 정보를 가져올 도시를 Seoul로 설정함
CITY = "Seoul"

# OpenWeatherMap API 요청 주소를 생성함
# q=Seoul: 서울 날씨 요청
# appid={API_KEY}: 본인의 API 키 사용
# units=metric: 섭씨 온도 단위 사용
# lang=kr: 날씨 설명을 한국어로 받을 수 있도록 설정
url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
)


# ------------------------------------------------------------
# 텍스트를 음성으로 출력하는 함수
# ------------------------------------------------------------

def speak(option, msg):
    """
    espeak를 이용하여 문자열을 음성으로 출력하는 함수

    option: espeak 음성 옵션
    msg: 음성으로 출력할 문장
    """

    # subprocess.run()을 이용해 터미널 명령어를 실행함
    # ["espeak", 옵션들..., msg] 형태로 실행하면 문자열 처리 오류를 줄일 수 있음
    subprocess.run(["espeak"] + option.split() + [msg])


# ------------------------------------------------------------
# 현재 서울 날씨 정보를 가져오는 함수
# ------------------------------------------------------------

def get_weather_message():
    """
    OpenWeatherMap API로 서울의 현재 날씨 정보를 요청하고,
    기온과 습도를 포함한 한글 안내 문장을 만들어 반환하는 함수
    """

    # OpenWeatherMap API에 GET 요청을 보냄
    # timeout=5는 5초 이상 응답이 없으면 요청을 중단하도록 설정함
    response = requests.get(url, timeout=5)

    # HTTP 응답 상태 코드가 오류일 경우 예외를 발생시킴
    # 예: API 키 오류, 네트워크 오류, 잘못된 요청 등
    response.raise_for_status()

    # API 응답 데이터를 JSON 형식으로 변환함
    data = response.json()

    # JSON 데이터에서 현재 기온 정보를 가져옴
    # data["main"]["temp"]에는 섭씨 온도가 저장되어 있음
    temp = data["main"]["temp"]

    # JSON 데이터에서 현재 습도 정보를 가져옴
    # data["main"]["humidity"]에는 습도 값이 저장되어 있음
    humidity = data["main"]["humidity"]

    # 기온은 소수점이 나올 수 있으므로 int()로 정수 형태로 변환함
    temp = int(temp)

    # 음성으로 출력할 한글 문장을 생성함
    msg = f"현재 서울의 날씨 정보입니다. 기온은 {temp}도, 습도는 {humidity}퍼센트입니다."

    # 완성된 안내 문장을 반환함
    return msg


# ------------------------------------------------------------
# 메인 프로그램 시작
# ------------------------------------------------------------

try:
    # Ctrl + C를 누르기 전까지 계속 음성 입력을 기다리는 무한 반복문
    while True:

        # Recognizer 객체를 생성함
        # 이 객체가 마이크 음성을 인식하고 텍스트로 변환하는 역할을 함
        recognizer = sr.Recognizer()

        # 기본 마이크를 입력 장치로 사용함
        # with문을 사용하면 마이크 사용이 끝난 뒤 자동으로 자원이 정리됨
        with sr.Microphone() as source:

            # 사용자에게 음성을 입력하라는 안내 문구를 출력함
            print("Listening... 말해주세요.")

            # 주변 소음에 맞춰 마이크 입력 기준을 조정함
            # 실습 환경이 시끄러울 때 인식률을 조금 높이는 데 도움이 됨
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # 마이크로부터 사용자의 음성을 입력받음
            # 입력된 음성 데이터는 audio 변수에 저장됨
            audio = recognizer.listen(source)

        try:
            # Google Speech Recognition을 사용하여 음성을 한국어 텍스트로 변환함
            # language='ko-KR'은 한국어 음성 인식을 의미함
            text = recognizer.recognize_google(audio, language="ko-KR")

            # 인식된 텍스트를 터미널에 출력함
            print("인식된 텍스트:", text)

            # 인식된 문장 안에 "날씨"라는 단어가 포함되어 있는지 확인함
            # 예: "날씨", "오늘 날씨 알려줘", "서울 날씨" 등도 인식 가능
            if "날씨" in text:

                # 날씨 명령이 인식되었음을 터미널에 출력함
                print("날씨 음성을 인식하였습니다.")

                # OpenWeatherMap API를 통해 현재 서울 날씨 문장을 생성함
                weather_msg = get_weather_message()

                # 생성된 날씨 안내 문장을 터미널에 출력함
                print(weather_msg)

                # espeak 음성 출력 옵션을 설정함
                # -s 180: 음성 속도
                # -p 50 : 음성 높낮이
                # -a 200: 음량
                # -v ko+f5: 한국어 여성 음성 설정
                option = "-s 180 -p 50 -a 200 -v ko+f5"

                # 날씨 안내 문장을 음성으로 출력함
                speak(option, weather_msg)

            else:
                # "날씨"라는 단어가 없으면 날씨 정보를 요청하지 않음
                print("날씨 명령이 아닙니다. 다시 말해주세요.")

        except sr.UnknownValueError:
            # 음성은 입력되었지만 Google Speech Recognition이 내용을 이해하지 못한 경우
            print("음성을 인식하지 못했습니다. 다시 말해주세요.")

        except sr.RequestError as e:
            # Google Speech Recognition 서비스에 요청하지 못한 경우
            # 인터넷 연결 문제나 API 요청 오류일 수 있음
            print(f"Google Speech Recognition 요청 실패: {e}")

        except requests.exceptions.RequestException as e:
            # OpenWeatherMap API 요청 과정에서 오류가 발생한 경우
            # 인터넷 연결, API 키, URL 문제 등을 확인해야 함
            print(f"날씨 정보 요청 실패: {e}")

        except KeyError:
            # API 응답 JSON 구조가 예상과 다를 때 발생함
            # API 키 오류 또는 잘못된 응답일 가능성이 있음
            print("날씨 데이터 형식이 올바르지 않습니다. API 키와 응답 내용을 확인하세요.")

        # 너무 빠르게 반복되지 않도록 1초 대기함
        time.sleep(1)

except KeyboardInterrupt:
    # 사용자가 Ctrl + C를 누르면 프로그램을 종료함
    print("\n프로그램을 종료합니다.")