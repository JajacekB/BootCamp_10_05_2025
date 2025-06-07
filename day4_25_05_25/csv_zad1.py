# pliki .csv

import csv
from datetime import date, timedelta


row = ["Radek", "Coe", "3", 0]
fields = ['name', 'branch', 'year', 'cgpa']

# połaczenie kolekcji i rzutowanie na słownik
zipped_dict = dict(zip(fields, row))
print(zipped_dict)
print(type(zipped_dict))

with open("dane/records.csv", "w", newline="") as csv_f:
    csvwriter = csv.writer(csv_f)
    csvwriter.writerow(row)

with open("dane/records_2.csv", "w", newline="") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(fields)
    csvwriter.writerow(row)

with open("dane/records_3.csv", "w", newline="") as csv_f:
    csv_dict_writer = csv.DictWriter(csv_f, fieldnames=fields)
    csv_dict_writer.writeheader()
    csv_dict_writer.writerow(zipped_dict)

today = date.today()
tomorrow = today + timedelta(days=1)


products = [
    {"sku": 1, 'exp_date': today, "price": 100},
    {"sku": 2, 'exp_date': today, "price": 200},
    {"sku": 3, 'exp_date': tomorrow, "price": 499.99},
    {"sku": 4, 'exp_date': today, "price": 50},
    {"sku": 5, 'exp_date': tomorrow, "price": 80},
]
# wyciagnięcie kluczy ze słownika umieszczonego w liście
fields_product = [k for k in products[0]]
with open("dane/records_discount.csv", 'w', newline="") as discount:
    csv_dict_writer = csv.DictWriter(discount, fieldnames=fields_product, delimiter=";")
    csv_dict_writer.writeheader()
    csv_dict_writer.writerows(products) # z literką 's' bo zapisujemy listę