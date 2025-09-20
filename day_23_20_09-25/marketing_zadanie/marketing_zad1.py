import numpy as np
import pandas as pd

df = pd.read_csv('marketing_r.csv', sep=",")

print(df)

print(df.describe())

df.info()

print(df['converted'].dtype) # object

df['converted'] = df['converted'].astype(bool)
print(df['converted'].dtype)
df.info()

print(df.head(1).to_string())

df['is_house_ads'] = np.where(df['marketing_channel'] == "House Ads", True, False)
print(df.is_house_ads.head(3))

df.to_csv('marketing_is_house_ads.csv', sep=",", index=False)