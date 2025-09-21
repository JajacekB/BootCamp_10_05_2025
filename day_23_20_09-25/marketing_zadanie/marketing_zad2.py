import numpy as np
import pandas as pd


df = pd.read_csv('marketing_r.csv', sep=",")
# print(df.head(1).to_string())

# sprawdzmy jaki typ m kolumna 'converted'
print(df['converted'].dtype)  # object

df['is_house_ads'] = np.where(df['marketing_channel'] == "House Ads", True, False)
print(df.is_house_ads.head(3))

# zmienić typ kolumny na typ bool
df['converted'] = df['converted'].astype('bool')
print(df['converted'].dtype)  # bool
df.info()

df['date_served'] = pd.to_datetime(df['date_served'], errors='coerce', format='mixed')
print(df['date_served'].head(3))

channel_dict = {"House Ads": 1, "Instagram": 2, "Facebook": 3, "Email": 4, "Push": 5}
df['channel_code'] = df['marketing_channel'].map(channel_dict)
print(df['channel_code'].head(3))

daily_users = df.groupby(['date_served'])['user_id'].nunique()
print("Dziennie:", daily_users)

df.to_csv("marketing_ok_date.csv")

subscribers = df[df['converted'] == True]['user_id'].nunique()
total = df['user_id'].nunique()
print("Subscribers:", subscribers)
print("Total", total)

conv_rate = subscribers / total
print("Convert rate", conv_rate)
print('Convert rate:', round(conv_rate * 100, 2), "%")

retained = df[df["is_retained"] == True]['user_id'].nunique()
retained = retained / subscribers
print("Retention:", round(retained * 100, 2), "%")

house_ads = df[df["subscribing_channel"] == "House Ads"]
retained = house_ads[house_ads["is_retained"] == True]["user_id"].nunique()
subscribers = house_ads[house_ads["converted"] == True]["user_id"].nunique()
retension_rate = retained / subscribers
print("Retention Rate:", round(retension_rate * 100, 2), "5")

retained = df[df["is_retained"] == True].groupby(['subscribing_channel'])["user_id"].nunique()
print(retained)

subscribers = df[df['converted'] == True].groupby(['subscribing_channel'])['user_id'].nunique()
print(subscribers)

channel_retention_rate = (retained / subscribers) * 100
print(channel_retention_rate)

import matplotlib.pyplot as plt

channel_retention_rate.plot(kind="bar")
plt.title("Wskaźnik utrzymania wg kanału")
plt.xlabel("Kanał", size=14)
plt.ylabel("Konwersja (%)", size=14)
plt.xticks(rotation=45)

plt.show()


