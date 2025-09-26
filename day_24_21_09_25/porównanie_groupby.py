import time
import dask.dataframe as dd
import polars as pl
import pandas as pd

filename = 'bigfile_polars.csv'

start = time.time()
df = pd.read_csv(filename)
result = df.groupby("category")['value'].sum()
print("Pandas groupby:", result)
print("Czas:", time.time() - start)


start = time.time()
df = pl.read_csv(filename)
result = df.group_by("category").agg(pl.col("value").sum())
print("Polars groupby:", result)
print("Czas:", time.time() - start)


start = time.time()
df = pl.scan_csv(filename)
result = (
    pl.scan_csv(filename)
    .group_by("category")
    .agg(pl.col("value").sum())
    .collect()
)

print("Polars lazy result:", result)
print("Czas:", time.time() - start)


start = time.time()
df = dd.read_csv(filename)

result = df.groupby("category")["value"].sum().compute()
print("Dask result:", result)
print("Czas:", time.time() - start)


