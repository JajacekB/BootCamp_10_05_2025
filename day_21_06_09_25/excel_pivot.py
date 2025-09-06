from openpyxl import Workbook
import openpyxl

wb = Workbook()
ws = wb.active
ws.title = "Dane"

data = [
    ["Data", "Kategoria", "Produkr", "Sprzedaj"],
    ["2024-01-01", "Elektronika", "Telefon", 1500],
    ["2024-01-02", "Elektronika", "Telefon", 1500],
    ["2024-01-02", "Odzieź", "Koszula", 50],
    ["2024-01-03", "Odzież", "Kurtka", 200],
    ["2024-01-04", "Elektronika", "Laptop", 1500],
]

for row in data:
    ws.append(row)

pivot_ws = wb.create_sheet("Tabela Przestawna")

wb.save("tabela_przestawna.xlsx")

# Dodawanie arkusza z danymi
ws = wb.add_worksheet("Dane")
ws.write_row('A1', data[0])  # Nagłówki
for row_num, row in enumerate(data[1:], start=1):
    ws.write_row(f'A{row_num + 1}', row)  # Wiersze danych

# Dodawanie arkusza, gdzie będzie tabela przestawna
pivot_ws = wb.add_worksheet("Tabela Przestawna")

# Tworzenie tabeli przestawnej
pivot_table_range = 'A1:D6'  # Zakres danych
pivot_table_location = 'A1'  # Lokalizacja tabeli przestawnej w nowym arkuszu

# Tworzymy obiekt PivotTable
pivot_table = pivot_ws.add_pivot_table(
    pivot_table_location,
    range=pivot_table_range,
    rows=['Kategoria'],  # Kolumny wierszy
    columns=['Produkt'],  # Kolumny
    values={'Sprzedaj': 'sum'},  # Agregacja danych
)