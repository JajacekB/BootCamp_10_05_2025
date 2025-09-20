import pandas as pd

df = pd.read_csv('data_with_date.csv')
print(df)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed')
print(df.to_string())

df = pd.read_csv('data_with_date.csv')
df.dropna(subset=['Date'], inplace= True)
print(df.to_string())


