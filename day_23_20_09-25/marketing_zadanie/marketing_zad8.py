import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from funkcion_tools import lift
from scipy import stats

# df = pd.read_csv('marketing_ok_date.csv', sep=",")
df = pd.read_csv('marketing_is_house_ads.csv', sep=",")
print(df.head(3))
print(df['date_served'].dtype)  # object
# df['date_served'] = pd.to_datetime(df['date_served'], format='%Y-%m-%d')
df['date_served'] = pd.to_datetime(df['date_served'], format='%m/%d/%y')
print(df.head(3))

email = df[df['marketing_channel'] == 'Email']
print(email.head().to_string())

alloc = email.groupby(['variant'])['user_id'].nunique()
print(alloc.head())

# alloc.plot(kind="bar")
# plt.title("Personalizacja testu")
# plt.ylabel("liczba")
# plt.show()

subscribers = email.groupby(['user_id', 'variant'])['converted'].max()
print(subscribers.head())

subscribers_df = pd.DataFrame(subscribers.unstack(level=1))
control = subscribers_df['control'].dropna()
print("Proba:", control.head())

control.info()

personalization = subscribers_df['personalization'].dropna()
print(personalization.tail())

print("Control conversion rate", np.mean(control))
print("Personalization conversion rate:", np.mean(personalization))

print("Lift:", lift(control, personalization))

def ab_segmantation(segment):
    for subsegment in np.unique(df[segment].values):
        print(subsegment)

    email = df[(df["marketing_channel"] == 'Email') & (df[segment] == subsegment)]
    print(email.head().to_string())

    subscribers = email.groupby(['user_id', 'variant'])['converted'].max()
    print(subscribers.head())
    subscribers = pd.DataFrame(subscribers.unstack(level=1))

    control = subscribers['control'].dropna()
    personalization = subscribers['personalization'].dropna()
    print(control.dtype, personalization.dtype)

    print("Lift:", lift(control, personalization))
    control = control.astype(int)
    personalization = personalization.astype(int)
    print("T-satic:", stats.ttest_ind(control, personalization), '\n\n')

ab_segmantation('language_displayed')
ab_segmantation('age_group')

