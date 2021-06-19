from collections import defaultdict
from datetime import datetime, time
from web import send_notification, import_data
from db_communication import send_metrics_to_db, send_f_measure_dependency
import numpy as np
import time
import gc


def get_raw_dictionary(raw_data):  # Преобразование сырых данных в словарь
    dictionary = defaultdict(list)
    for i in range(0, len(raw_data), 6):
        if i == len(raw_data):
            break
        else:
            dictionary.setdefault(int(int(raw_data[i + 3])), []).append(int(int(raw_data[i + 1]) / 1000))
            dictionary.setdefault(int(raw_data[i + 3]), []).append(raw_data[i + 5])
            i += 6
    dictionary = dict(dictionary)
    return dictionary


def get_indexes(actions_dictionary):  # Получение индексов неполной матрицы истинности: TP, FP, их альтернативы и FN
    TP = 0
    FP = 0
    FN = 0
    conversion_incomplete = 0
    for key in dict(actions_dictionary):
        if 'PURCHASE' in actions_dictionary[key] and 'CONVERSION' in actions_dictionary[key]:
            TP += 1
        if 'PURCHASE' in actions_dictionary[key] and 'CONVERSION' not in actions_dictionary[key]:
            FN += 1
        if 'CLOSE' in actions_dictionary[key]:
            FP += 1
        if 'CONVERSION' in actions_dictionary[key] and 'PURCHASE' not in actions_dictionary[key]:
            conversion_incomplete += 1
        if (len(actions_dictionary[key]) == 2) and (actions_dictionary[key][1] == 'RECOMENDATION'):
            FP += 1
        key += 1
    TP_Conv = TP + conversion_incomplete
    FP_Conv = FP + conversion_incomplete
    return TP, TP_Conv, FP, FP_Conv, FN


def get_precision(indexes):  # Подсчёт точности
    try:
        precision = indexes[0] / (indexes[0] + indexes[3])
    except ZeroDivisionError:
        return 0
    return precision


def get_precision_alt(indexes):  # Альтернативный подсчёт точности
    try:
        precision_alt = indexes[1] / (indexes[1] + indexes[2])
    except ZeroDivisionError:
        return 0
    return precision_alt


def get_recall(indexes):  # Подсчёт полноты
    try:
        recall = indexes[0] / (indexes[0] + indexes[4])
    except ZeroDivisionError:
        return 0
    return recall


def get_recall_alt(indexes):  # Альтернавтивный подсчёт полноты
    try:
        recall_alt = indexes[1] / (indexes[1] + indexes[4])
    except ZeroDivisionError:
        return 0
    return recall_alt


def get_beta_f_measure(indexes, beta):  # Подсчёт F-меры
    try:
        beta_f_measure = (1 + beta * beta) * (indexes[0] / (indexes[0] + indexes[3])) * (indexes[0] /
                                                                                         (indexes[0] + indexes[4])) / \
                         ((beta * beta * (indexes[0] / (indexes[0] + indexes[3]))) + (indexes[0] / (indexes[0] +
                                                                                                    indexes[4])))
    except ZeroDivisionError:
        return 0
    return beta_f_measure


def get_beta_f_measure_alt(indexes, beta):  # Альтернативный подсчёт F-меры
    try:
        beta_f_measure_alt = (1 + beta * beta) * (indexes[1] / (indexes[1] + indexes[2])) * (indexes[1] /
                                                                                             (indexes[1] +
                                                                                              indexes[4])) \
                             / ((beta * beta * (indexes[1] / (indexes[1] + indexes[2]))) + (indexes[1] / (indexes[1] +
                                                                                                          indexes[4])))
    except ZeroDivisionError:
        return 0
    return beta_f_measure_alt


def get_all_metrics(indexes, beta):  # Подсчёт всех метрик разом
    try:
        precision = indexes[0] / (indexes[0] + indexes[3])
        precision_alt = indexes[1] / (indexes[1] + indexes[2])
        recall = indexes[0] / (indexes[0] + indexes[4])
        recall_alt = indexes[1] / (indexes[1] + indexes[4])
        beta_f_measure = (1 + beta * beta) * precision * recall / ((beta * beta * precision) + recall)
        beta_f_measure_alt = (1 + beta * beta) * precision_alt * recall_alt / ((beta * beta * precision_alt) + recall_alt)
    except ZeroDivisionError:
        print("Denominator must not be 0")
    return precision, precision_alt, recall, recall_alt, beta_f_measure, beta_f_measure_alt


def get_summary(indexes, metrics):  # Текстовая сводка по всем данным
    summary = ("\nTP: {}\n"
               "FP: {}\n"
               "Оборванных на Conversion цепочек: {}\n"
               "Precision: {}\n"
               "Precision alternative: {}\n"
               "Recall: {}\n"
               "Recall alternative: {}\n"
               "F-Мера: {}\n"
               "F-Мера alternative: {}\n").format(indexes[0], indexes[2], (indexes[1] - indexes[0]), *metrics)
    return summary


def get_beta_f_measure_dependency(indexes):  # Возвращает лист из кортежей, состоящих из beta и beta_f_measure
    dependency_graph = []
    for beta in np.arange(0.00, 5.00, 0.01):
        beta_f_measure = (1 + beta * beta) * (indexes[0] / (indexes[0] + indexes[3])) * (indexes[0] /
                                                                                         (indexes[0] + indexes[4])) / \
                         ((beta * beta * (indexes[0] / (indexes[0] + indexes[3]))) + (indexes[0] / (indexes[0] +
                                                                                                    indexes[4])))
        dependency_graph.append((float(format(round(beta, 2), '.2f')), float(beta_f_measure)))
    return dependency_graph


def main():
    timing = time.time()
    while True:
        if time.time() - timing > 1800.0:

            timestamp = datetime.now()
            indexes = get_indexes(get_raw_dictionary(import_data(timestamp)))
            metrics = get_all_metrics(indexes, 1)
            send_metrics_to_db(indexes, metrics, timestamp)
            # send_f_measure_dependency(get_beta_f_measure_dependency(indexes))
            timing = time.time()
            del timestamp, indexes, metrics
            gc.collect()


if __name__ == '__main__':
    main()
