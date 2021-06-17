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
