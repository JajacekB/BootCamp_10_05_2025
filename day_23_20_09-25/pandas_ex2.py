import pandas as pd

df= pd.read_csv("data.csv")
print(df)

print(df.to_string())

print(pd.options.display.max_rows)

pd.options.display.max_rows = 250
print(df)

pd.options.display.max_rows = 60
print(df)


