import time
import pandas as pd
import polars as pl
import dask.dataframe as dd

filename = "bigfile_polars.csv"

# Polars (read)
start = time.time()
df_polars = pl.read_csv(filename)
filtered_polars = df_polars.filter(pl.col("category") == "B")
print("Polars: liczba wierszy z kategorią 'B':", filtered_polars.height)
print("Polars filter czas:", time.time() - start)


# polars (scan, czyli lazy - nie tryma całego pliku w RAM
start = time.time()
df_polars = pl.scan_csv(filename)
filtered_polars = df_polars.filter(pl.col("category") == "B").collect()
print("Polars: liczba wierszy z kategorią 'B':", filtered_polars.height)
print("Polars filter czas:", time.time() - start)

start = time.time()
df_pandas = pd.read_csv(filename)
filtered_pandas = df_pandas[df_pandas['category'] == "B"]
print("Pandas: liczba wierszy z kategorią 'B':", len(filtered_pandas))
print("Pandas filter czas:", time.time() - start)

df = dd.read_csv(filename)

filtered_dask = df[df["category"] == "B"]

start = time.time()
result = filtered_dask.shape[0].compute()
end = time.time()

print("Dask: liczba wierszy z kategorią 'B':", result)
print("Dask filter czas:", end - start)