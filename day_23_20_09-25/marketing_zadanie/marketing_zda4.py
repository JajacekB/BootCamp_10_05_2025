import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("marketing_ok_date.csv", sep=",")

language_age = df.groupby(["language_preferred", "age_group"])["user_id"].count()
language_age = pd.DataFrame(language_age.unstack(level=0))
print(language_age.head())

# language_age.plot()
# plt.title("Preferencje Wiekowe")
# plt.xlabel("Wiek")
# plt.ylabel("Użytkownicy")
# plt.legend(loc="upper right", labels=language_age.columns.values)
#
# plt.show()
#
language_age.plot(kind="bar")
plt.title("Preferencje Wiekowe")
plt.xlabel("Wiek")
plt.ylabel("Użytkownicy")
plt.legend(loc="upper right", labels=language_age.columns.values)

plt.show()
