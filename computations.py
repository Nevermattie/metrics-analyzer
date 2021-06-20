from collections import defaultdict
import numpy as np


# Преобразование сырых данных в словарь с ключами из INN
def get_raw_dictionary(raw_data):
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


# Получение индексов неполной матрицы истинности: TP, FP, их альтернативы и FN
def get_indexes(actions_dictionary):
    TP = 0
    FP = 0
    FN = 0
    conversion_incomplete = 0
    for key in dict(actions_dictionary):
        if 'PURCHASE' in actions_dictionary[key] and 'CONVERSION' in actions_dictionary[key]:
            TP += 1
        elif 'PURCHASE' in actions_dictionary[key] and 'CONVERSION' not in actions_dictionary[key]:
            FN += 1
        elif 'CLOSE' in actions_dictionary[key]:
            FP += 1
        elif 'CONVERSION' in actions_dictionary[key] and 'PURCHASE' not in actions_dictionary[key]:
            conversion_incomplete += 1
        elif (len(actions_dictionary[key]) == 2) and (actions_dictionary[key][1] == 'RECOMENDATION'):
            FP += 1
        key += 1
    TP_Conv = TP + conversion_incomplete
    FP_Conv = FP + conversion_incomplete
    return TP, TP_Conv, FP, FP_Conv, FN


# Подсчёт Precision отдельно
def get_precision(indexes):
    try:
        precision = indexes[0] / (indexes[0] + indexes[3])
    except ZeroDivisionError:
        return 0
    return precision


# Альтернативный подсчёт Precision отдельно
def get_precision_alt(indexes):
    try:
        precision_alt = indexes[1] / (indexes[1] + indexes[2])
    except ZeroDivisionError:
        return 0
    return precision_alt


# Подсчёт Recall отдельно
def get_recall(indexes):
    try:
        recall = indexes[0] / (indexes[0] + indexes[4])
    except ZeroDivisionError:
        return 0
    return recall


# Альтернативный подсчёт Recall отдельно
def get_recall_alt(indexes):
    try:
        recall_alt = indexes[1] / (indexes[1] + indexes[4])
    except ZeroDivisionError:
        return 0
    return recall_alt


# Подсчёт F-score - среднего гармонического Recall и Precision, отдельно
def get_beta_f_measure(indexes, beta):
    try:
        beta_f_measure = (1 + beta * beta) * (indexes[0] / (indexes[0] + indexes[3])) * (indexes[0] /
                                                                                         (indexes[0] + indexes[4])) / \
                         ((beta * beta * (indexes[0] / (indexes[0] + indexes[3]))) + (indexes[0] / (indexes[0] +
                                                                                                    indexes[4])))
    except ZeroDivisionError:
        return 0
    return beta_f_measure


# Альтернативный подсчёт F-score, отдельно
def get_beta_f_measure_alt(indexes, beta):
    try:
        beta_f_measure_alt = (1 + beta * beta) * (indexes[1] / (indexes[1] + indexes[2])) * (indexes[1] /
                                                                                             (indexes[1] +
                                                                                              indexes[4])) \
                             / ((beta * beta * (indexes[1] / (indexes[1] + indexes[2]))) + (indexes[1] / (indexes[1] +
                                                                                                          indexes[4])))
    except ZeroDivisionError:
        return 0
    return beta_f_measure_alt


# Подсчёт всех метрик разом, для удобства
def get_all_metrics(indexes, beta):
    try:
        precision = indexes[0] / (indexes[0] + indexes[3])
        precision_alt = indexes[1] / (indexes[1] + indexes[2])
        recall = indexes[0] / (indexes[0] + indexes[4])
        recall_alt = indexes[1] / (indexes[1] + indexes[4])
        beta_f_measure = (1 + beta * beta) * precision * recall / ((beta * beta * precision) + recall)
        beta_f_measure_alt = (1 + beta * beta) * precision_alt * recall_alt / ((beta * beta * precision_alt) +
                                                                               recall_alt)
    except ZeroDivisionError:
        print("Denominator must not be 0")
    return precision, precision_alt, recall, recall_alt, beta_f_measure, beta_f_measure_alt


# Текстовая сводка по всем данным, на всякий случай
def get_summary(indexes, metrics):
    summary = ("\nTP: {}\n"
               "FP: {}\n"
               "Оборванных на Conversion цепочек: {}\n"
               "Precision: {}\n"
               "Precision альтернативное: {}\n"
               "Recall: {}\n"
               "Recall альтернативное: {}\n"
               "F-score: {}\n"
               "F-score альтернативное: {}\n").format(indexes[0], indexes[2], (indexes[1] - indexes[0]), *metrics)
    return summary


# Возвращает зависимость F-меры от beta: лист из кортежей, состоящих из beta и f_measure
def get_beta_f_measure_dependency(indexes):
    dependency_graph = []
    for beta in np.arange(0.00, 5.00, 0.01):
        beta_f_measure = (1 + beta * beta) * (indexes[0] / (indexes[0] + indexes[3])) * (indexes[0] /
                                                                                         (indexes[0] + indexes[4])) / \
                         ((beta * beta * (indexes[0] / (indexes[0] + indexes[3]))) + (indexes[0] / (indexes[0] +
                                                                                                    indexes[4])))
        dependency_graph.append((float(format(round(beta, 2), '.2f')), float(beta_f_measure)))
    return dependency_graph
