import sqlite3

sql_connection = None

try:
    sql_connection = sqlite3.connect("sqlite_python.db")
    cursor = sql_connection.cursor()
    print("Baza danych została połączona")

    insert = """
    INSERT INTO software (id,name,price) VALUES (1,'Python',100);
    """

    insert2 = """
        INSERT INTO software (id,name,price) VALUES (2,'Java',1000);
        """

    insert3 = """
        INSERT INTO software (id,name,price) VALUES (3,'C++',1200);
        """

    insert4 = """
        INSERT INTO software (id,name,price) VALUES (4,'Python',2300);
        """

    # cursor.execute(insert)
    # cursor.execute(insert2)
    # cursor.execute(insert3)
    # cursor.execute(insert4)

    # sql_connection.commit()

    select = """
    SELECT * FROM software;
    """

    for row in cursor.execute(select):
        print(row)

    cursor.execute(select)
    rows = cursor.fetchall()
    print(rows)

except sqlite3.Error as e:
    print("Błąd bazy danych", e)
finally:
    if sql_connection:
        sql_connection.close()
        print("Baza danych została zamknięta")