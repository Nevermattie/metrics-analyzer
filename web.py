import requests
import re
import io


def send_notification(self):
    API_link = "https://api.telegram.org/bot1885420798:AAFlz0IBlmzylgLaR9Iurkx8S1r7GX8hGLQ"
    text = str(self)
    chat_id = -495488219
    requests.get(API_link + f"/sendMessage?chat_id={chat_id}&text={text}")


def import_data():  # Запрос статистики за конкретный период
    headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
    url = 'http://localhost:8080/execmodel'
    dates = {'start': '01.01.2010', 'finish': '31.12.2021'}
    urlData = requests.post(url, json=dates, headers=headers)
    testData = io.StringIO(urlData.json())
    parsed_data = re.findall(r'\w+', testData.readline().replace('\n', ''))
    testData.close()
    urlData.close()
    return parsed_data
