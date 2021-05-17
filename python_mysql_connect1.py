import mysql.connector
from mysql.connector import Error
from mysql.connector import MySQLConnection, Error


def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='python_mysql',
                                       user='root',
                                       password='password')
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)


def insert_books(books):
    query = "INSERT INTO test_db_2(inn, datetime, action)"
            "VALUES(%s,%s,%s)"


    conn_insert = connect()
    try:
        cursor = conn_insert.cursor()
        cursor.executemany(query, books)

        conn_insert.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn_insert.close()

def main():
    connect()
    books = [('Harry Potter And The Order Of The Phoenix', '9780439358071'),
             ('Gone with the Wind', '9780446675536'),
             ('Pride and Prejudice (Modern Library Classics)', '9780679783268')]
    insert_books(books)

if __name__ == '__main__':
    main()

