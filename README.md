## Методология подсчёта метрик
Распарсив исходные данные становится известно, что возможно несколько вариантов цепочек действий пользователя:
1. `Recommendations` - считаем однозначно как FP
2. `Recommendations -> Purchase` - считаем как FN
3. `Recommendations -> Conversion` - однозначно нельзя сказать как считать, поэтому считаем отдельно и потом складываем либо с TP, либо c FP. 
В исходных данных **TP_conv** или же **TP_alternative** представляет собой сумму TP и количества таких оборванных на Conversion цепочек.
Аналогично с **FP_conv** / **FP_alternative**
4. `Recommendations -> Conversion -> Purchase` - однозначно TP
5. `Recommendations -> Close` - однозначно FP

## Взаимодействие с базой данных
Данные об индексах и посчитанных метриках отправляются в MySQL. Формат таблицы:

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
