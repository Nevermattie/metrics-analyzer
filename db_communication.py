import mysql.connector
from mysql.connector import MySQLConnection, Error
from db_config import read_db_config


def connect():
    """ Connect to MySQL database """
    try:
        # conn = mysql.connector.connect(host='{}'.format(input("host: ")), database='{}'.format(input("database:")),
        #                                user='{}'.format(input("user: ")), password='{}'.format(input("password: ")))
        mydb = mysql.connector.connect(host='{}'.format("localhost"), database='{}'.format("db_metrics"),
                                       user='{}'.format("root"), password='{}'.format("password"))
        if mydb.is_connected():
            print('Connected to database db_metrics')
    except Error as e:
        print(e)


def insert_metrics(indexes, metrics, timestamp):
    query = """INSERT INTO table_metrics(TP,TP_alternative,FP,FP_alternative,FN,Prec,Precision_alternative,Recall,Recall_alternative,F1score,F1score_alternative,Updated) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    args = (indexes[0], indexes[1], indexes[2], indexes[3], indexes[4], metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], timestamp)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


def query_with_fetchall():
    try:
        dbconfig = read_db_config()
        mydb = MySQLConnection(**dbconfig)
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM raw_data")
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()
