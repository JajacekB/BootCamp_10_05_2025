import sqlite3

from day10_29_06_25.baza3 import insert

data = [
    (6, "Rust", 899),
    (7, "Angular", 1899),
    (8, "JS", 99),
]

sql_connection = None

try:
    sql_connection = sqlite3.connect("sqlite_python.db")
    cursor = sql_connection.cursor()
    print("Baza danych została połączona")

    insert = """
    INSERT INTO software (id,name,price) VALUES (?,?,?);
    """
    #cursor.execute(insert, (5, "Scala", 5600))
    #sql_connection.commit()

    cursor.executemany(insert, data)
    sql_connection.commit()

except sqlite3.Error as e:
    print("Błąd bazy danych", e)
finally:
    if sql_connection:
        sql_connection.close()
        print("Baza danych została zamknięta")