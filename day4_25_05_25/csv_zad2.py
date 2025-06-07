import csv

columns = []
rows = []

filename = 'dane/records_3.csv'  # wiele wierszy
# filename = 'dane/records_discount.csv'  # wiele wierszy oddzielone ;

with open(filename, "r") as f:
    dialect = csv.Sniffer().sniff(f.read(1024))  # odczytamy 1024 znaki by sprawdzic znak podziału
    print(dialect)  # <class 'csv.Sniffer.sniff.<locals>.dialect'>
    print(dialect.delimiter)  # ;
    print(dialect.quotechar)  # "

    f.seek(0)  # odczyt na początek pliku
    # StopIteration - dane z iteratora zostały wykorzystane
    csvreader = csv.reader(f, delimiter=dialect.delimiter)
    # csvreader = csv.reader(f, delimiter=";")
    # csvreader = csv.reader(f)

    print(csvreader)  # <_csv.reader object at 0x10412d380>
    # iterator - mozna uzywac go na sekwencji
    # pozwala wczytywac pojedyncze dane
    columns = next(csvreader)  # next()  - odczyt pojedynczego elemntu, pierwszy wiersz
    # kolejne odczytanie iteratora następeje od kolejnego elementu
    for row in csvreader:  # zacznie od drugiego wiersza
        # print(row)
        rows.append(row)

print("Columns:", columns)
print("Rows:", rows)
# <_csv.reader object at 0x102744d60>
# Columns: ['name', 'branch', 'year', 'cgpa']
# Rows: [['Radek', 'Coe', '3', '0']]
# Columns: ['sku;exp_date;price']
# Rows: [['1;2025-05-25;100'], ['2;2025-05-25;200'],
# ['3;2025-05-26;499.99'], ['4;2025-05-25;50'], ['5;2025-05-26;80']]
# delimiter=";"
# Columns: ['sku', 'exp_date', 'price']
# Rows: [['1', '2025-05-25', '100'], ['2', '2025-05-25', '200'],
# ['3', '2025-05-26', '499.99'], ['4', '2025-05-25', '50'],
#        ['5', '2025-05-26', '80']]
# automatyczny delimiter
# Columns: ['sku', 'exp_date', 'price']
# Rows: [['1', '2025-05-25', '100'], ['2', '2025-05-25', '200'],
# ['3', '2025-05-26', '499.99'],
# ['4', '2025-05-25', '50'], ['5', '2025-05-26', '80']]
# niezależnie od znaku podziąlu dane wczytują sie prawidłowo
# Columns: ['name', 'branch', 'year', 'cgpa']
# Rows: [['Radek', 'Coe', '3', '0']]