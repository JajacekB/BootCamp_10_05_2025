import sqlite3

sql_connection = None

try:
    sql_connection = sqlite3.connect("sqlite_python.db")
    cursor = sql_connection.cursor()
    print("Baza danych została połączona")
except sqlite3.Error as e:
    print("Błąd bazy danych", e)
finally:
    if sql_connection:
        sql_connection.close()
        print("Baza danych została zamknięta")