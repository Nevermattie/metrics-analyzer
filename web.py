import requests
import re
import io


def send_notification(self):    # Отправляет текстовое уведомление в телеграм-чат через бота
    try:
        API_link = "https://api.telegram.org/botXXXXXXXXXX:YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
        text = str(self)
        chat_id = -000000000    # Тут указывается id чата
        requests.get(API_link + f"/sendMessage?chat_id={chat_id}&text={text}")
    except Exception as error:
        print('\033[1;31m' + 'Something went wrong. Check the send_notification()' + '\033[0m')


def import_data(timestamp):  # Запрос статистики за конкретный период: принимает datetime, возвращает статистику
    headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
    url = 'http://localhost:8080/execmodel'
    dates = {'start': '01.01.2010', 'finish': '{}'.format(timestamp.date().strftime("%d.%m.%Y"))}
    urlData = requests.post(url, json=dates, headers=headers)
    testData = io.StringIO(urlData.json())
    parsed_data = re.findall(r'\w+', testData.readline().replace('\n', ''))
    testData.close()
    urlData.close()
    return parsed_data
