import requests
import xml.etree.ElementTree as ET
from pydantic import BaseModel
from typing import List
from datetime import datetime

url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=xml"

response = requests.get(url)
print(response)
print(response.text)

xml_data = response.content

root = ET.fromstring(xml_data)
print(root)

table_name = root.find(".//Table").text
print(f"Tabela: {table_name}")

date = root.find(".//EffectiveDate").text
print(f"Data tabeli: {date}")

no = root.find(".//No").text
print(f"Numer tabeli: {no}")

rates = root.findall(".//Rate")
print(rates)

for rate in rates:
    concurent = rate.find("Currency").text
    code = rate.find("Code").text
    mid = rate.find("Mid").text
    print(f"{code} : {concurent} - {mid}")  # # THB : bat (Tajlandia) - 0.1109


class Rate(BaseModel):
    currency: str
    code: str
    mid: float



class ExchangeRatesTable(BaseModel):
    table: str
    data: datetime
    number: str
    rates: List[Rate]



currency_rates = []

for rate in rates:
    currency = rate.find("Currency").text
    code = rate.find("Code").text
    mid = rate.find("Mid").text
    print(f"{code} : {currency} - {mid}")  # # THB : bat (Tajlandia) - 0.1109

    currency_rates.append(Rate(currency=currency, code=code, mid=float(mid)))

date = datetime.strptime(date, "%Y-%m-%d")
exchange_rate = ExchangeRatesTable(
    table=table_name,
    data=date,
    number=no,
    rates=currency_rates
)
