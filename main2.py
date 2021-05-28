import requests
import re
import io
from collections import defaultdict
from pprint import pprint
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from python_mysql_connect1 import *
from python_mysql_dbconfig import *


# Запрос статистики за конкретный период
headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'
dates = {'start': '01.01.2018', 'finish': '01.06.2019'}
urlData = requests.post(url, json=dates, headers=headers)
testData = io.StringIO(urlData.json())
testParse = re.findall(r'\w+', testData.readline().replace('\n', ''))

dictDates = defaultdict(list)  # Пустой словарь с ключами из datetime
dictInns = defaultdict(list)   # Пустой словарь с ключами из INN


# mydb = mysql.connector.connect(host='{}'.format("localhost"),   database='{}'.format("db_metrics"),
#                                user='{}'.format("root"),        password='{}'.format("password"))

# mycursor.execute('CREATE TABLE raw_data (datetime TIMESTAMP, inn BIGINT(20), action VARCHAR(20))')


i = 1
# while i <= len(testParse):
#     if testParse[i + 4] == 'RECOMENDATION':
#         insert_raw_data("""INSERT INTO raw_data (datetime, inn, activity)
#                 VALUES('{}',{},'{}')""".format(str(datetime.fromtimestamp(int(int(testParse[i])/1000))),
#                                                int(testParse[i + 2]),
#                                                str('RECOMMENDATION')))
#     else:
#         insert_raw_data("""INSERT INTO raw_data (datetime, inn, activity)
#                             VALUES('{}',{},'{}')""".format(str(datetime.fromtimestamp(int(int(testParse[1])/1000))),
#                                                            int(testParse[i + 2]),
#                                                            testParse[i + 4]))
#     i += 6

# print(type(query_with_fetchall()))
pprint(testParse)
