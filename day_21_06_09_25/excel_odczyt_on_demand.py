import xlrd

with xlrd.open_workbook('xlwt.xls', on_demand=True) as book:
    sheet = book.sheet_by_index(0)

print(sheet)
print(sheet.name)
print(sheet.nrows)

