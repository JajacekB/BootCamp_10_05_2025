import pandas as pd

df = pd.read_csv("data.csv")
print(df.info())

df.fillna(130, inplace=True)
print(df.info())

print(df.loc[141])
