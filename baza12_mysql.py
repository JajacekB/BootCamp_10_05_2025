import mysql.connector
from mysql.connector import Error


try:
    connection = mysql.connector.connect(
        host='',
        port=3380,  # standartowy port dla mysql=3306
        database='',
        user='',
        password=''
    )


    if connection.is_connected():
        # db_info = connection.get_server_info()
        db_info = connection.server_info
        print("Połaczeno z serwers MySql w wersji:", db_info)

        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchall()
        print("Połaczono z bazą danych:", record)

except Error as e:
    print("Bład podczas połaczenia do bazy danych:", e)

finally:
    if connection.is_connected():
        connection.close()
        print("Połaczenie z MySsl zostało zamknięte")