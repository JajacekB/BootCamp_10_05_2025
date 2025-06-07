from datetime import date, datetime, timedelta

today = date.today()
print(today)
print(type(today))

time = datetime.now()
print(time)
print(type(time))

print("Godzina: ", time.hour)
print("Dzień: ", today.day)

formated_date = datetime.now().strftime("%d/%m/%Y")
print("Dzisiejsza data: ", formated_date)

formated_time = datetime.now().strftime("%H:%M:%S")
print("Aktualna godzina: ", formated_time)
print("Aktualna godzina: ", formated_time.removeprefix("0"))

formated_time_USA = datetime.now().strftime("%I:%M:%S %p")
print("Godzina w formacie USA: ", formated_time_USA)
print(type(formated_time_USA))

time_from_str = datetime.now().strptime("25/05/2025", "%d/%m/%Y")
print("data ze stringu: ", time_from_str)
print(type(time_from_str))

tomorrow = today + timedelta(days=1)
print("Jutro będzie: ", tomorrow)


print("-----Biedronka-----")

products = [
    {"sku": 1, 'exp_date': today, "price": 100},
    {"sku": 2, 'exp_date': today, "price": 200},
    {"sku": 3, 'exp_date': tomorrow, "price": 499.99},
    {"sku": 4, 'exp_date': today, "price": 50},
    {"sku": 5, 'exp_date': tomorrow, "price": 80},
]

print(products[0]["price"])

for product in products:
#     print(product)
#     print(product["exp_date"])

#     if product['exp_date'] == today:
#         product["price"] *= 0.8
#         print(product['price'])
    if product['exp_date'] != today:
        continue
        # końćzy bieżące wykonanie pętli, nakazuje pobrać kolejny eleemnt, wraca na początek

    product["price"] *= 0.8
    print(f"""Price for sku: {product['sku']}, date: {product["exp_date"]}
is now: {product['price']}""")