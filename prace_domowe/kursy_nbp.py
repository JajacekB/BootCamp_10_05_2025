# z api nbp kurs złota
# dzienny, historyczny

import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Rate(BaseModel):
    no: str
    effectiveDate: datetime
    mid: float


class Gold(BaseModel):
    data: datetime
    cena: float


class Waluta(BaseModel):
    table: str
    currency: str
    code: str
    rates: List[Rate]


class NBPClient:
    def __init__(self, base_url = "https://api.nbp.pl/api", date: str = None):
        """

        :param base_url:
        :param date:
        """


    def load_input_currency(self):

        self.table = "A"

        print("""Jaką walutę chcesz sprawdzić podaj kod waluty:
        USD - Dolar amerykański
        EUR - Euro
        CHF - Frank szwajcarskie
        GBP - Funt szterling (brytyjski)
        JPY - Jen japoński
        CZK - Korona czeska
        NOK - Korona norweska
        SEK - Korona szwecka
        DKK - Korona duńska
        CAD - Dolar kanadyjski
        AUD - Dolar australijski
        CNY - Juan chiński
        """)
        valid_currency_codes = [
            "USD", "EUR", "CHF", "GBP", "JPY", "CZK",
            "NOK", "SEK", "DKK", "CAD", "AUD", "CNY"
        ]
        while True:
            self.code = input("\nPodaj kod waluty: ").strip().upper()
            if self.code in valid_currency_codes:
                break
            print("\nNiepoprawny kod waluty. Spróbuj ponownie.")

        while True:
            date_input = input("\nPodaj datę kursu waluty (RRRR-MM-DD) (Naciśnij ENTER jesli chcesz dzisiajszą: ").strip()

            if date_input =="":
                self.date = None
                break

            try:
                parsed_date = datetime.date(date_input, "%Y-%m-%d").date()
                stat_date = datetime.date("2002-01-02", "%Y-%m-%d").date()
                today = datetime.today().date()

                if stat_date <= parsed_date <= today:
                    self.date = date_input
                    break
                else:
                    print(f"\nData musi być z zakresu {stat_date} - {today}. Spróbuj ponownie")
            except ValueError:
                print("\nNiepoprawny format daty, użyj formatu RRRR-MM-DD")

    def load_input_gold(self):
        while True:
            date_input = input("\nPodaj datę ceny złota (RRRR-MM-DD) (Naciśnij ENTER jesli chcesz dzisiajszą: ").strip()

            if date_input =="":
                self.date = None
                break

            try:
                parsed_date = datetime.date(date_input, "%Y-%m-%d").date()
                stat_date = datetime.date("2013-01-02", "%Y-%m-%d").date()
                today = datetime.today().date()

                if stat_date <= parsed_date <= today:
                    self.date = date_input
                    break
                else:
                    print(f"\nData musi być z zakresu {stat_date} - {today}. Spróbuj ponownie")
            except ValueError:
                print("\nNiepoprawny format daty, użyj formatu RRRR-MM-DD")

    def get_currency_rate(self):

        url = self.build_url_currency()
        response = requests.get(url)
        response_data = response.json()

        currency_data = Waluta(**response_data)
        effectiveDate = currency_data.rates[0].effectiveDate
        formated_date = effectiveDate.strftime("%d/%m/%Y")

        print(f"""
        Kurs waluty: ({currency_data.code}) {currency_data.currency}
        na dzień: {formated_date}
        wynosi: {currency_data.rates[0].mid} zł""")

    def build_url_currency(self):
        elements = [
            self.base_url,
            "exchangerates",
            "rates",
            self.table.strip("/"),
            self.code.strip("/").lower(),
            self.date
        ]
        url = "/".join(filter(None, elements))
        return url

    def get_gold_price(self):

        url = self.build_url_gold()
        response = requests.get(url)
        response_data = response.json()

        gold = Gold(**response_data[0])
        gold_date = gold.data
        formated_gold_date = gold_date.strftime("%d/%m/%Y")

        print(f"""
        Cena złota (Gold)
        na dzień: {formated_gold_date}
        wynosi: {gold.cena}""")

    def build_url_gold(self):
        elements = [
            self.base_url,
            "cenyzlota",
            self.date
        ]
        url = "/".join(filter(None, elements))
        return url

    def send_request(self, url: str) -> dict:
        """

        :param url:
        :return:
        """

