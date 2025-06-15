import requests
from pydantic import BaseModel
from typing import List
from datetime import datetime

# url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR/?format=json"
url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR/"

response = requests.get(url)
print(response)
print(response.text)

table = response.json()
print(table)
print(type(table))

print(f"Waluta: {table['currency']}")
print(f"Rates: {table.get('rates')}")

print(f"""
Kurs waluty: {table['currency']}
na dzień: {table['rates'][0]['effectiveDate']}
wynosi: {table['rates'][0]['mid']} zł""")


class Rate(BaseModel):
    no: str
    # effectiveDate: str
    effectiveDate: datetime
    mid: float

class Waluta(BaseModel):
    table: str
    currency: str
    code: str
    rates: List[Rate]


currency_data = Waluta(**table)
print(currency_data)


print(currency_data.currency)
print(currency_data.code)
print(currency_data.rates[0])
print(currency_data.rates[0].mid)
print(currency_data.rates[0].effectiveDate)

print(type(currency_data.rates[0].effectiveDate))
effectiveDate = currency_data.rates[0].effectiveDate
formated_date = effectiveDate.strftime("%d/%m/%Y")
print(F"Datat tabeli {formated_date}")