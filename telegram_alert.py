import requests

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=data, timeout=10)

        if response.status_code == 200:
            print("Telegram Alert Sent")
        else:
            print("Telegram Error:", response.text)

    except Exception as e:
        print("Telegram Error:", e)
