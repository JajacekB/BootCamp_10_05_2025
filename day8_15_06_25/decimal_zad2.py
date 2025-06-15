from decimal import Decimal

def calculate_gross_price(net_price, vat):
    net_price = Decimal(net_price)
    vat_rate = Decimal(vat) / 100
    gross_price = net_price + (net_price * vat_rate)

    return gross_price.quantize(Decimal("0.01"))

price_netto = "100.99"
vat = 23
price_brutto = calculate_gross_price(price_netto, vat)

print(f"""
Cena netto: {price_netto}
Vat: {vat}
Cena brutto: {price_brutto}
""")
