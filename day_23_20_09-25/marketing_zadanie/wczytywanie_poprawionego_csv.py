import pandas as pd

df = pd.read_csv('marketing_r.csv')
print(df.head().to_string())
df = pd.read_csv('marketing_r.csv', sep=",")
print(df.head(1).to_string())

