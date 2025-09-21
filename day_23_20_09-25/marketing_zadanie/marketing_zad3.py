import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('marketing_ok_date.csv', sep=",")
print(df.head(3))

language = df.groupby(["date_served", "language_preferred"])["user_id"].count()
print(language.head())

language = pd.DataFrame(language.unstack(level=1))
print(language.head())

language.plot()
plt.title("Dzienne preferencje językowe")
plt.xlabel("Data")
plt.ylabel("Użytkownicy")
plt.legend(loc="upper right", labels=language.columns.values)

plt.show()


