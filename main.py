import requests
import re
import io
from collections import defaultdict
from pprint import pprint
import datetime

# Запрос статистики за конкретный период
headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'
dates = {'start': '01.01.2018', 'finish': '01.06.2019'}
urlData = requests.post(url, json=dates, headers=headers)
testData = io.StringIO(urlData.json())
testParse = re.findall(r'\w+', testData.readline().replace('\n', ''))

dictDates = defaultdict(list)  # Пустой словарь с ключами из datetime
dictInns = defaultdict(list)   # Пустой словарь с ключами из INN

i = 1
while i <= len(testParse):
    # Проверяет наличие ключа datetime в dictDates с элементом-списком и добавляет в список inn
    dictDates.setdefault(int(int(testParse[i])/1000), []).append(int(int(testParse[i + 2])))

    # Проверяет наличие ключа datetime в dictDates с элементом-списком и добавляет в список действие
    dictDates.setdefault(int(int(testParse[i])/1000), []).append(testParse[i + 4])\

    # Проверяет наличие ключа-inn в dictInns с элементом-списком и добавляет в список datetime
    dictInns.setdefault(int(int(testParse[i + 2])), []).append(int(int(testParse[i])/1000))

    # Проверяет наличие ключа-inn в dictInns с элементом-списком и добавляет в список действие
    dictInns.setdefault(int(testParse[i + 2]), []).append(testParse[i + 4])
    i += 6

dictInns = dict(dictInns)
dictDates = dict(dictDates)

# На выходе получим словарь dictDates формата:
# { datetime:[inn, действие],
#   datetime:[inn, действие], ...}

# И ещё один словарь dictInns формата:
# { inn:[datetime, действие, datetime2, действие2],
#   inn:[datetime, действие], ...}

indexTP = 0     # Учёт выборки True Positive
indexFP = 0     # Учёт выборки False Positive

for key in dict(dictInns):
    if 'PURCHASE' in dictInns[key]:
        indexTP += 1
    if 'CLOSE' in dictInns[key]:
        indexFP += 1
    key += 1

indexPrecision = indexTP / (indexTP + indexFP)  # Расчёт индекса Precision
print(indexPrecision)
