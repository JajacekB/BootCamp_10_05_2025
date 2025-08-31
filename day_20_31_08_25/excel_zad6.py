import pyexcel

data = [
    ["imię", "Wiek"],
    ["tomek", 45],
    ["Kasia", 34]
]

sheet = pyexcel.Sheet(data)
sheet.save_as("wyniki.xlsx")

sheet = pyexcel.get_sheet(file_name='wyniki.xlsx')
print(sheet)