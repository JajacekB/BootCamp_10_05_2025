import xlrd
# from xlwt.Utils import cell_to_rowcol2

person = xlrd.open_workbook('dane_person.xls')
print(person)

print(person.sheet_names())

sheet = person.sheet_by_index(0)
print(sheet.name)

sheet = person.sheet_by_name("Arkusz1")
print(sheet.name)

print(sheet.nrows)
print(sheet.ncols)

print(sheet.cell(1, 0).value)