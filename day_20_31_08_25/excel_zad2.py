import xlsxwriter
import datetime as dt


book = xlsxwriter.Workbook("xlsxwriter.xls")

sheet = book.add_worksheet("Arkusz")

sheet.write("A1", 'Witaj 1')
sheet.write("A2", 'Witaj 2')

formatting = book.add_format(
    {"font_color":"#FF0000",
     "bg_color":"#FFFF00",
     "bold": True,
     "align": "center",
     "border": 1,
     "border_color":"#FF0000"
    }
)
sheet.write("A3", "Witaj 3", formatting)

date_format = book.add_format({"num_format": "yyyy/mm/dd"})
sheet.write("A4", dt.date(2016, 10, 13), date_format)

number_format = book.add_format({"num_format": "0.00"})
sheet.write("A5", 3.333333, number_format)

sheet.write("A6", "=SUM(A4, 2)")

sheet.insert_image(0, 6, "django_komendy.png") #, {"x_scale": 0.5, "y_scale": 0.5})

categories = ["Styczeń", "Luty"]
values = [100, 200]
sheet.write_row("B10", categories)
sheet.write_row('B11', values)

chart = book.add_chart({"type" : "column"})
chart.set_title({"name" : "Sprzedaż"})
chart.add_series(
    {
        "name": "=Arkusz!A11",
        "categories": "=Arkusz!B10:C10",
        "values": "=Arkusz!B11:C11"
    }
)

chart.set_x_axis({"name": "Os X"})
chart.set_y_axis({"name": "Os Y"})

sheet.insert_chart("A20", chart)

book.close()