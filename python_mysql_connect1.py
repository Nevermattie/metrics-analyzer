import mysql.connector
from mysql.connector import Error
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import *


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


def insert_raw_data(query):
    try:
        db_config = read_db_config()
        mydb = MySQLConnection(**db_config)

        cursor = mydb.cursor()
        cursor.execute(query)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        mydb.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        mydb.close()


def query_with_fetchall():
    try:
        dbconfig = read_db_config()
        mydb = MySQLConnection(**dbconfig)
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()
