# Методология подсчёта метрик
Распарсив исходные данные становится известно, что возможно несколько вариантов цепочек действий пользователя:
1. `Recommendations` - считаем однозначно как FP
2. `Recommendations -> Purchase` - считаем как FN
3. `Recommendations -> Conversion` - однозначно нельзя сказать как считать, поэтому считаем отдельно и потом складываем либо с TP, либо c FP. 
В исходных данных **TP_conv** или же **TP_alternative** представляет собой сумму TP и количества таких оборванных на Conversion цепочек.
Аналогично с **FP_conv** / **FP_alternative**
4. `Recommendations -> Conversion -> Purchase` - однозначно TP
5. `Recommendations -> Close` - однозначно FP

# Структура проекта
Внутри файлов есть комментарии, содержащие краткие комментарии о работе тех или иных методов

`start.py` - отвечает за настройку и запуск скрипта по обновлению данных

`computations.py` - содержит методы для обработки входных данных и расчёта метрик и индексов. 

`web.py` - содержит метод для отправки уведомлений через бота в телеграм и импорта данных с сервера

`db_config.py` - содержит вспомогательный метод, считывающий данные базы данных из **config.ini** и использующий их в **db_communication.py**

`db_communication.py` - методы для взаимодействия с базой данных

# Взаимодействие с базой данных
Данные об индексах и посчитанных метриках отправляются в базу данных (Нами использовалась MySQL). Формат таблицы следующий:

Column | Type
------ | ----
F1score | float
F1score_alternative | float
FN | int
FP | int
FP_alternative | float
Prec | float
Precision_alternative | float
Recall | float
Recall_alternative | flaot
TP | int
TP_alternative | int
Updated | datetime
