import requests


def send_notification(self, datetime):
    API_link = "https://api.telegram.org/bot1885420798:AAFlz0IBlmzylgLaR9Iurkx8S1r7GX8hGLQ"
    text = "Тестовая сводка за {} // \n {}".format(datetime, self)
    chat_id = -495488219
    requests.get(API_link + f"/sendMessage?chat_id={chat_id}&text={text}")

