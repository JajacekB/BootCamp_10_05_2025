import matplotlib.pyplot as plt
import pandas as pd
from IPython.core.pylabtools import figsize

df = pd.read_csv('data/data.csv')

# print(df)
# print(df['data'])

df['date'] = pd.to_datetime(df.date, format="%d/%m/%Y")
x = df['date']
y = df["Close"]

lista = [100, 999]

figure, ax = plt.subplots(2, figsize=(10, 4))
ax[0].scatter(x, y, marker="+", alpha=.5)
_ = ax[1].pie(lista, labels=['wpłata', 'wypłata'])
_ = ax[1].legend

plt.show()




