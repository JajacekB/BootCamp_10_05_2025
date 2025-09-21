import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("marketing_ok_date.csv", sep=",")

retention_total = df["user_id"].nunique()
print(retention_total)

retention_total = df.groupby(['date_subscribed', 'subscribing_channel'])['user_id'].nunique()
print(retention_total.head(3))

retention_subs = df[df['is_retained'] == True].groupby(['date_subscribed', 'subscribing_channel'])['user_id'].nunique()
print(retention_subs.head(5))


retention_rate = retention_subs / retention_total
print(retention_rate.head(5))

retention_rate = pd.DataFrame(retention_rate.unstack(level=1))
print(retention_rate.tail())

retention_rate.plot()
plt.title("Data w zależności od kanału")
plt.xlabel("Data")
plt.ylabel("Uzytkownicy")
plt.legend(loc="upper right", labels=["E", "F", "HA", "I", "P"])

plt.show()



