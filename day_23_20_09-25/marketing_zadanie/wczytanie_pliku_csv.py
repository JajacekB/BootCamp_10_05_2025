import pandas as pd

df = pd.read_csv('marketing_przecinek.csv', sep=",", nrows=1)
print(df)
print(df.columns)
df.columns = df.columns.str.replace(" ", "")

# df_new = df.copy()
# print(df_new)
# print(df_new.columns)

lista_kolumn = df.columns.tolist()
print(lista_kolumn)

df = pd.read_csv('marketing_przecinek.csv',
                sep=r"\s{2,}",
                engine= "python",
                skiprows=1,
                header=None,
                names=lista_kolumn
                )

print(df.head())
print(df.head(1).to_string())

df.to_csv('marketing_r.csv', sep=",", index=False)