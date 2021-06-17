import requests
import re
import io
from collections import defaultdict
from datetime import datetime, date, time
from python_mysql_connect1 import *
from telegram_notify import send_notification
from pprint import pprint
import timeit


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


def raw_dictionary(raw_data):  # Подготовка данных
    dictionary = defaultdict(list)  # Пустой словарь с ключами из INN
    for i in range(0, len(raw_data), 6):
        if i == len(raw_data):
            break
        else:
            dictionary.setdefault(int(int(raw_data[i + 3])), []).append(int(int(raw_data[i + 1]) / 1000))
            dictionary.setdefault(int(raw_data[i + 3]), []).append(raw_data[i + 5])
            i += 6
    dictionary = dict(dictionary)
    return dictionary


def confusion_matrix(dictionary):   # Получение индексов неполной матрицы истинности
    tp = 0
    fp = 0
    fn = 0
    conversion_incomplete = 0
    for key in dict(dictionary):
        if 'PURCHASE' in dictionary[key] and 'CONVERSION' in dictionary[key]:
            tp += 1
        if 'PURCHASE' in dictionary[key] and 'CONVERSION' not in dictionary[key]:
            fn += 1
        if 'CLOSE' in dictionary[key]:
            fp += 1
        if 'CONVERSION' in dictionary[key] and 'PURCHASE' not in dictionary[key]:
            conversion_incomplete += 1
        if (len(dictionary[key]) == 2) and (dictionary[key][1] == 'RECOMENDATION'):
            fp += 1
        key += 1
    tp_alt = tp + conversion_incomplete
    fp_alt = fp + conversion_incomplete
    return tp, tp_alt, fp, fp_alt, fn


def get_precision(indexes):  # Подсчёт точности
    precision = indexes[0] / (indexes[0] + indexes[3])
    return precision


def get_precision_alt(indexes):  # Альтернативный подсчёт точности
    precision = indexes[1] / (indexes[1] + indexes[2])
    return precision


def get_recall(indexes):    # Подсчёт полноты
    recall = indexes[0] / (indexes[0] + indexes[4])
    return recall


def get_recall_alt(indexes):    # Альтернавтивный подсчёт полноты
    recall_alt = indexes[1] / (indexes[1] + indexes[4])
    return recall_alt


def get_beta_f_measure(indexes, beta):  # Подсчёт F-меры
    BetaFMeasure = (1 + beta * beta) * \
                   (indexes[0] / (indexes[0] + indexes[3])) * \
                   (indexes[0] / (indexes[0] + indexes[4])) / \
                   ((beta * beta * (indexes[0] / (indexes[0] + indexes[3]))) +
                    (indexes[0] / (indexes[0] + indexes[4])))
    return BetaFMeasure


def get_beta_f_measure_alt(indexes, beta):  # Альтернативный подсчёт F-меры
    BetaFMeasureAlt = (1 + beta * beta) * \
                      (indexes[1] / (indexes[1] + indexes[2])) * (indexes[1] / (indexes[1] + indexes[4])) \
                      / ((beta * beta * (indexes[1] / (indexes[1] + indexes[2]))) +
                         (indexes[1] / (indexes[1] + indexes[4])))
    return BetaFMeasureAlt


def get_metrics(tp, tp_alt, fp, fp_alt, fn, beta):  # Подсчёт всех метрик разом
    Precision = tp / (tp + fp_alt)
    PrecisionAlt = tp_alt / (tp_alt + fp)
    Recall = tp / (tp + fn)
    RecallAlt = tp_alt / (tp_alt + fn)
    BetaFMeasure = (1 + beta*beta) * Precision * Recall / ((beta*beta*Precision) + Recall)
    BetaFMeasureAlt = (1 + beta*beta) * PrecisionAlt * RecallAlt / ((beta*beta*PrecisionAlt) + RecallAlt)
    return Precision, PrecisionAlt, Recall, RecallAlt, BetaFMeasure, BetaFMeasureAlt


def get_summary(indexes, metrics):  # Сводка по всем данным
    summary = ("\nTP: {}\n"
               "FP: {}\n"
               "Оборванных на Conversion цепочек: {}\n"
               "Precision: {}\n"
               "Precision alternative: {}\n"
               "Recall: {}\n"
               "Recall alternative: {}\n"
               "F-Мера: {}\n"
               "F-Мера alternative: {}\n").format(indexes[0], indexes[2], (indexes[1]-indexes[0]),
                                                  *metrics)
    return summary


def main():
    timestamp = datetime.now()
    indexes = confusion_matrix(raw_dictionary(import_data()))
    metrics = get_metrics(indexes[0], indexes[1], indexes[2], indexes[3], indexes[4], 1)
    summary = get_summary(indexes, metrics)
    send_notification(summary, timestamp)


if __name__ == '__main__':
    main()

