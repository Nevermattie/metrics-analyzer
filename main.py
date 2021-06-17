import requests
import re
import io
from collections import defaultdict
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from python_mysql_connect1 import *
from telegram_notify import send_notification

# Запрос статистики за конкретный период
headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'
dates = {'start': '01.01.2018', 'finish': '01.06.2019'}
urlData = requests.post(url, json=dates, headers=headers)
testData = io.StringIO(urlData.json())
testParse = re.findall(r'\w+', testData.readline().replace('\n', ''))

dictDates = defaultdict(list)  # Пустой словарь с ключами из datetime
dictInns = defaultdict(list)   # Пустой словарь с ключами из INN


connect()


i = 1
while i <= len(testParse):
    # Проверяет наличие ключа-inn в dictInns с элементом-списком и добавляет в список datetime
    dictInns.setdefault(int(int(testParse[i + 2])), []).append(int(int(testParse[i])/1000))

    # Проверяет наличие ключа-inn в dictInns с элементом-списком и добавляет в список действие
    dictInns.setdefault(int(testParse[i + 2]), []).append(testParse[i + 4])
    print(i, " ", len(testParse))
    i += 6


dictInns = dict(dictInns)


# На выходе получим словарь dictDates формата:
# { datetime:[inn, действие],
#   datetime:[inn, действие], ...}

# И ещё один словарь dictInns формата:
# { inn:[datetime, действие, datetime2, действие2],
#   inn:[datetime, действие], ...}
# pprint(dictDates)
# pprint(dictInns)

TP = 0     # Учёт выборки True Positive
FP = 0     # Учёт выборки False Positive
FN = 0
ConversionAlt = 0

for key in dict(dictInns):
    if 'PURCHASE' in dictInns[key] and 'CONVERSION' in dictInns[key]:
        TP += 1
    if 'PURCHASE' in dictInns[key] and 'CONVERSION' not in dictInns[key]:
        FN += 1
    if 'CLOSE' in dictInns[key]:
        FP += 1
    if 'CONVERSION' in dictInns[key] and 'PURCHASE' not in dictInns[key]:
        ConversionAlt += 1
    if (len(dictInns[key]) == 2) and (dictInns[key][1] == 'RECOMENDATION'):
        FP += 1
    key += 1

beta = 1
Precision = (TP + ConversionAlt) / (TP + ConversionAlt + FP)  # Precision
PrecisionAlt = TP / (TP + FP + ConversionAlt)
Recall = TP / (TP + FN)
RecallAlt = (TP + ConversionAlt) / (TP + FN + ConversionAlt)
BetaFMeasure = (1 + beta*beta) * Precision * Recall / ((beta*beta*Precision) + Recall)

arguments = [TP, FP, Precision, PrecisionAlt, Recall, RecallAlt, BetaFMeasure]

summary = ("\nTP: {}\n"
           "FP: {}\n"
           "Precision (Точность): {}\n"
           "Precision alternative: {}\n"
           "Recall (Полнота): {}\n"
           "Recall alternative: {}\n"
           "F-Мера: {}").format(*arguments)




