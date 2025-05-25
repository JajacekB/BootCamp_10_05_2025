import csv

columns = []
rows = []

filename = 'dane/records_2.csv'

with open(filename, "r") as f:
    dialect = csv.Sniffer().sniff(f.read(1024))
    print(dialect)
    print(dialect.delimiter)
    print(dialect.quotechar)

    f.seek(0)

    csvreader = csv.reader(f, delimiter=dialect.delimiter)

    print(csvreader) # iterator

    columns = next(csvreader)

    for row in csvreader: # zacznie od 2 rzędu
        print(row)

print("Columns:", columns)
print("Rows:", row)