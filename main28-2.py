# OpenWeatherMap API를 호출하기 위해 사용하는 라이브러리입니다.
# 외부 URL로 요청을 보내고 응답 데이터를 받아올 때 사용합니다.
import urllib.request

# OpenWeatherMap에서 받은 JSON 데이터를 Python 딕셔너리 형태로 변환하기 위해 사용합니다.
import json

# 현재 날짜와 시간을 확인하기 위해 사용하는 라이브러리입니다.
import datetime

# 비동기 처리를 위해 사용하는 라이브러리입니다.
# Telegram 메시지 전송처럼 네트워크 요청이 필요한 작업을 효율적으로 처리할 수 있습니다.
import asyncio

# 운영체제 환경변수에서 API 키, 토큰, chat_id 값을 불러오기 위해 사용합니다.
import os

# .env 파일에 저장된 환경변수를 Python 코드에서 읽을 수 있게 해주는 라이브러리입니다.
from dotenv import load_dotenv

# Telegram Bot API를 Python에서 쉽게 사용할 수 있게 해주는 클래스입니다.
from telegram import Bot


# 현재 폴더에 있는 .env 파일을 읽어서 환경변수로 등록합니다.
load_dotenv()


# OpenWeatherMap API 키를 .env 파일에서 불러옵니다.
# 깃허브에 올릴 때는 실제 API 키를 코드에 직접 적으면 안 됩니다.
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# 텔레그램 봇 토큰을 .env 파일에서 불러옵니다.
# bot token은 Telegram Bot API에서 내 봇을 인증하기 위해 필요한 값입니다.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# 텔레그램 메시지를 받을 대상의 chat_id를 .env 파일에서 불러옵니다.
# chat_id는 메시지를 받을 사용자, 그룹, 채널을 구분하는 값입니다.
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# 날씨 정보를 조회할 도시 이름을 설정합니다.
# 이번 실험에서는 서울의 일기예보를 가져오도록 설정했습니다.
CITY_NAME = "Seoul"


# OpenWeatherMap API에서 사용할 단위 설정입니다.
# metric을 사용하면 온도가 섭씨 단위로 제공됩니다.
UNITS = "metric"


# OpenWeatherMap API에서 받을 언어 설정입니다.
# en은 영어 날씨 설명, kr은 한국어 날씨 설명에 사용할 수 있습니다.
LANGUAGE = "en"


# 가져올 예보 데이터 개수를 설정합니다.
# OpenWeatherMap의 forecast API는 보통 3시간 간격의 예보 데이터를 제공합니다.
# cnt=8은 3시간 간격 데이터 8개, 즉 약 24시간 예보를 의미합니다.
FORECAST_COUNT = 8


# 알림을 보낼 시간을 설정합니다.
# 원래 실험에서는 오전 7시부터 3시간 간격으로 알림이 가도록 구성했습니다.
# 예: 07시, 10시, 13시, 16시, 19시, 22시
ALERT_HOURS = [7, 10, 13, 16, 19, 22]


# 실험 확인용 알림 시간을 직접 지정할 수 있는 리스트입니다.
# 예를 들어 현재 시간이 11:08이면 "11:09"를 넣어서 1분 뒤 알림 전송을 테스트할 수 있습니다.
# 실제 사용 시에는 빈 리스트로 두어도 됩니다.
TEST_ALERT_TIMES = []


# Telegram Bot 객체를 생성합니다.
# 이 객체를 통해 텔레그램 서버에 메시지 전송 요청을 보낼 수 있습니다.
bot = Bot(token=TELEGRAM_BOT_TOKEN)


# OpenWeatherMap API에서 날씨 데이터를 가져오는 함수입니다.
def get_weather_message():
    # OpenWeatherMap forecast API 요청 URL을 생성합니다.
    # q에는 도시 이름, appid에는 API 키, units에는 단위, lang에는 언어, cnt에는 데이터 개수를 넣습니다.
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={CITY_NAME}"
        f"&appid={OPENWEATHER_API_KEY}"
        f"&units={UNITS}"
        f"&lang={LANGUAGE}"
        f"&cnt={FORECAST_COUNT}"
    )

    # 생성한 URL로 HTTP 요청을 보냅니다.
    # urllib.request.urlopen()은 해당 주소에 접속해서 응답을 받아옵니다.
    with urllib.request.urlopen(url) as response:
        # API 응답 데이터를 읽어옵니다.
        # response.read()는 바이트 형태의 데이터를 반환합니다.
        response_data = response.read()

        # 바이트 데이터를 JSON 형식으로 변환합니다.
        # json.loads()를 사용하면 Python 딕셔너리 형태로 사용할 수 있습니다.
        data = json.loads(response_data)

    # 텔레그램으로 보낼 최종 메시지를 저장할 문자열 변수입니다.
    message = ""

    # data["list"]에는 시간별 예보 데이터가 리스트 형태로 들어 있습니다.
    # FORECAST_COUNT가 8이므로 총 8개의 예보 데이터를 반복 처리합니다.
    for item in data["list"]:
        # dt_txt는 예보 시간이 들어 있는 문자열입니다.
        # 예: "2026-04-30 09:00:00"
        date_time_text = item["dt_txt"]

        # 시간 부분만 잘라냅니다.
        # "2026-04-30 09:00:00"에서 11~13번째 문자를 가져오면 "09"가 됩니다.
        hour = date_time_text[11:13]

        # main 안에 있는 temp 값을 가져옵니다.
        # temp는 해당 시간의 기온입니다.
        temperature = item["main"]["temp"]

        # main 안에 있는 humidity 값을 가져옵니다.
        # humidity는 해당 시간의 습도입니다.
        humidity = item["main"]["humidity"]

        # weather 리스트의 첫 번째 요소에서 description 값을 가져옵니다.
        # description은 clear sky, few clouds 같은 날씨 설명입니다.
        description = item["weather"][0]["description"]

        # 텔레그램에서 보기 좋은 형태로 한 줄의 날씨 정보를 만듭니다.
        # 예: (09h 21.5C 60% clear sky)
        line = f"({hour}h {temperature:.1f}C {humidity}% {description})"

        # 만든 한 줄의 날씨 정보를 전체 메시지에 추가합니다.
        # 줄바꿈 문자 \n을 붙여서 텔레그램에서 여러 줄로 보이게 합니다.
        message += line + "\n"

    # 완성된 날씨 메시지 문자열을 반환합니다.
    return message


# 현재 시간이 알림 시간인지 확인하는 함수입니다.
def is_alert_time(now):
    # 현재 시각의 시(hour)를 가져옵니다.
    current_hour = now.hour

    # 현재 시각의 분(minute)을 가져옵니다.
    current_minute = now.minute

    # 현재 시각을 "HH:MM" 형태의 문자열로 변환합니다.
    # 예: 11시 9분이면 "11:09"가 됩니다.
    current_hm = now.strftime("%H:%M")

    # TEST_ALERT_TIMES에 현재 시간이 들어 있으면 테스트용 알림 시간으로 판단합니다.
    # 실험할 때 현재 시간 1분 뒤를 넣으면 빠르게 결과를 확인할 수 있습니다.
    if current_hm in TEST_ALERT_TIMES:
        return True

    # 현재 시각의 시(hour)가 ALERT_HOURS에 포함되어 있고,
    # 현재 분이 0분이면 정규 알림 시간으로 판단합니다.
    if current_hour in ALERT_HOURS and current_minute == 0:
        return True

    # 위 조건에 해당하지 않으면 알림 시간이 아니므로 False를 반환합니다.
    return False


# 텔레그램으로 메시지를 전송하는 비동기 함수입니다.
async def send_telegram_message(text):
    # Telegram Bot API의 send_message 기능을 사용하여 메시지를 전송합니다.
    # chat_id는 메시지를 받을 대상이고, text는 전송할 메시지 내용입니다.
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)


# 프로그램의 핵심 동작을 담당하는 비동기 main 함수입니다.
async def main():
    # 사용자가 Ctrl + C를 누르기 전까지 계속 실행되도록 무한 반복문을 사용합니다.
    while True:
        # 현재 시간을 가져옵니다.
        now = datetime.datetime.now()

        # 현재 시간을 "HH:MM:SS" 형태로 변환합니다.
        # 터미널에서 현재 확인 중인 시간을 보기 위해 사용합니다.
        current_time_text = now.strftime("%H:%M:%S")

        # 현재 확인 중인 시간을 터미널에 출력합니다.
        print(f"현재 시간 확인 중: {current_time_text}")

        # 현재 시간이 알림 시간인지 확인합니다.
        if is_alert_time(now):
            # 알림 시간이 맞으면 OpenWeatherMap API에서 날씨 데이터를 가져와 메시지로 가공합니다.
            weather_message = get_weather_message()

            # 터미널에서도 전송할 메시지를 확인할 수 있도록 출력합니다.
            print("전송할 날씨 메시지:")
            print(weather_message)

            # 가공된 날씨 메시지를 텔레그램으로 전송합니다.
            await send_telegram_message(weather_message)

            # 같은 분 안에서 메시지가 여러 번 전송되는 것을 막기 위해 60초 동안 대기합니다.
            await asyncio.sleep(60)

        # 알림 시간이 아니면 1초마다 현재 시간을 다시 확인합니다.
        await asyncio.sleep(1)


# 이 파일을 직접 실행했을 때만 아래 코드가 실행됩니다.
# 다른 파일에서 import할 경우에는 자동 실행되지 않습니다.
if __name__ == "__main__":
    # 비동기 main 함수를 실행합니다.
    # asyncio.run()은 async 함수가 실제로 동작할 수 있게 이벤트 루프를 생성합니다.
    asyncio.run(main())