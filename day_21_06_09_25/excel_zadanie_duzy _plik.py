import openpyxl

import lxml

book = openpyxl.Workbook(write_only=True)

sheet = book.create_sheet()

for row in range(1000):
    sheet.append(list(range(200)))

book.save("openpyxl_optimized.xlsx")
