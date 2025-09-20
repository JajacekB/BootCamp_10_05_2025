import pandas as pd

df = pd.read_csv("data.csv")
print(df)
print(df.info())

new_df = df.dropna()
print(new_df.to_string())
print(new_df.info())

df.dropna(inplace=True)
print(df.info())

