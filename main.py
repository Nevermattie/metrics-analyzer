import requests
import re
import io
from collections import defaultdict
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from python_mysql_connect1 import *
from telegram_notify import send_notification
import timeit
from pprint import pprint


# Запрос статистики за конкретный период
def import_data():
    headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
    url = 'http://localhost:8080/execmodel'
    dates = {'start': '01.01.2018', 'finish': '01.06.2019'}
    urlData = requests.post(url, json=dates, headers=headers)
    testData = io.StringIO(urlData.json())
    parsed_data = re.findall(r'\w+', testData.readline().replace('\n', ''))
    return parsed_data


# Подготовка данных
def dict_inn(raw_data):
    dictInns = defaultdict(list)  # Пустой словарь с ключами из INN
    for i in range(0, len(raw_data), 6):
        if i == len(raw_data):
            break
        else:
            dictInns.setdefault(int(int(raw_data[i + 3])), []).append(int(int(raw_data[i + 1]) / 1000))
            dictInns.setdefault(int(raw_data[i + 3]), []).append(raw_data[i + 5])
            i += 6
    dictInns = dict(dictInns)
    return dictInns


# dictInns = dict(dictInns)


# На выходе получим словарь dictDates формата:
# { datetime:[inn, действие],
#   datetime:[inn, действие], ...}

# И ещё один словарь dictInns формата:
# { inn:[datetime, действие, datetime2, действие2],
#   inn:[datetime, действие], ...}
# pprint(dictDates)
# pprint(dictInns)

# TP = 0     # Учёт выборки True Positive
# FP = 0     # Учёт выборки False Positive
# FN = 0
# TP_alt = 0
# FP_alt = 0
# ConversionAlt = 0
#
#
# for key in dict(dictInns):
#     if 'PURCHASE' in dictInns[key] and 'CONVERSION' in dictInns[key]:
#         TP += 1
#     if 'PURCHASE' in dictInns[key] and 'CONVERSION' not in dictInns[key]:
#         FN += 1
#     if 'CLOSE' in dictInns[key]:
#         FP += 1
#     if 'CONVERSION' in dictInns[key] and 'PURCHASE' not in dictInns[key]:
#         ConversionAlt += 1
#     if (len(dictInns[key]) == 2) and (dictInns[key][1] == 'RECOMENDATION'):
#         FP += 1
#     key += 1
#
# TP_alt = TP + ConversionAlt
# FP_alt = FP + ConversionAlt
# beta = 1
#
# Precision = TP / (TP + FP)  # Precision
# PrecisionAlt = TP_alt / (TP_alt + FP_alt)
# Recall = TP / (TP + FN)
# RecallAlt = TP_alt / (TP_alt + FN)
# BetaFMeasure = (1 + beta*beta) * Precision * Recall / ((beta*beta*Precision) + Recall)
# BetaFMeasureAlt = (1 + beta*beta) * PrecisionAlt * RecallAlt / ((beta*beta*PrecisionAlt) + RecallAlt)
#
# arguments = [TP, FP, Precision, PrecisionAlt, Recall, RecallAlt, BetaFMeasure, BetaFMeasureAlt]
#
# summary = ("\nTP: {}\n"
#            "FP: {}\n"
#            "Precision (Точность): {}\n"
#            "Precision alternative: {}\n"
#            "Recall (Полнота): {}\n"
#            "Recall alternative: {}\n"
#            "F-Мера: {}\n"
#            "F-Мера alternative: {}\n").format(*arguments)

if __name__ == '__main__':
    pprint(dict_inn(import_data()))
