import numpy as np
import pandas as pd
from sympy import rotations


df = pd.read_csv('marketing_r.csv', sep=",")

print(df.describe())


df.info()

print(df['converted'].dtype)  # object

# zmienić typ kolumny na typ bool
df['converted'] = df['converted'].astype('bool')
print(df['converted'].dtype)  # bool
df.info()

print(df.head(1).to_string())

df['is_house_ads'] = np.where(df['marketing_channel'] == "House Ads", True, False)
print(df.is_house_ads.head(3))

df.to_csv('marketing_is_house_ads.csv', sep=",", index=False)

# zamiana dat na typ datetime
df['date_served'] = pd.to_datetime(df['date_served'], errors='coerce', format='mixed')
print(df['date_served'].head(3))
# 0   2018-01-01
# 1   2018-01-01
# 2   2018-01-01
# Name: date_served, dtype: datetime64[ns]

# # dni tygodnia numerycznie
# df['date_served'] = df['date_served'].dt.dayofweek
# print(df['date_served'].head(3))
# # 0    0.0 - poniedziałek
# # 1    0.0
# # 2    0.0
# # Name: date_served, dtype: float64

# nazwy dni tygodnia
# df['day_name'] = df['date_served'].dt.day_name()
# print(df['day_name'].head(3))
# 0    Monday
# 1    Monday
# 2    Monday
# Name: day_name, dtype: object
# dodanie kolumny channel_code, zmapowanie nazw  marketing_channel na channel_code
channel_dict = {"House Ads": 1, "Instagram": 2, "Facebook": 3, "Email": 4, "Push": 5}
df['channel_code'] = df['marketing_channel'].map(channel_dict)
print(df['channel_code'].head(3))
# 0    1.0
# 1    1.0
# 2    1.0
# Name: channel_code, dtype: float64

# unikalni uzytkownicy dziennie
daily_users = df.groupby(['date_served'])['user_id'].nunique()
print("Dziennie:", daily_users)


import matplotlib.pyplot as plt

daily_users.plot()

plt.title("Zasięg dzienny kampani marketingowej")
plt.xlabel("Data")
plt.ylabel("Liczba użytkowników")
plt.xticks(rotation=45)

plt.show()
