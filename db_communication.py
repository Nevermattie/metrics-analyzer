from mysql.connector import MySQLConnection, Error
from db_config import read_db_config


# Отправляет одну строку со всеми данными в table_metrics
def send_metrics_to_db(indexes, metrics, timestamp):
    query = """INSERT INTO table_metrics(TP,TP_alternative,FP,FP_alternative,FN,Prec,Precision_alternative,Recall,Recall_alternative,F1score,F1score_alternative,Updated) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    args = (indexes[0], indexes[1], indexes[2], indexes[3], indexes[4], metrics[0],
            metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], timestamp)
    try:
        conn = MySQLConnection(**read_db_config())
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as error:
        print(error)
    finally:
        print('\033[92m'+'{}  1 row of data has been sent to [db_metrics].[table_metrics] '.format(timestamp)+'\033[0m')
        cursor.close()
        conn.close()


# Обновляет данные в таблице table_dependency
def send_f_measure_dependency(dependency_graph):
    clear = """TRUNCATE TABLE db_metrics.table_dependency;"""
    query = """INSERT INTO table_dependency(beta,fmeasure)
            VALUES(%s,%s)"""
    try:
        conn = MySQLConnection(**read_db_config())
        cursor = conn.cursor()
        cursor.execute(clear)
        conn.commit()
        conn.cursor()
        cursor.executemany(query, dependency_graph)
        conn.commit()
        print('\033[92m' + 'Table [db_metrics].[table_dependency] has been updated' + '\033[0m')
    except Error as e:
        print('\033[1;31m' + 'Error: ', e, '\033[0m')
    finally:
        cursor.close()
        conn.close()


def truncate_table_metrics():   # Очищает таблицу table_metrics с данными
    query = "TRUNCATE TABLE db_metrics.table_metrics;"
    try:
        conn = MySQLConnection(**read_db_config())
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print('\033[1;31m' + "Table [table_metrics] has been cleared successfully" + '\033[0m')
    except Error as e:
        print('\033[1;31m' + 'Error: ', e, '\033[0m')
    finally:
        cursor.close()
        conn.close()
