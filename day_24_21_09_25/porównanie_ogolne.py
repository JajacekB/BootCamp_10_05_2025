import time
import dask.dataframe as dd
import polars as pl
import pandas as pd

filename = 'bigfile_polars.csv'

start = time.time()
df = pd.read_csv(filename)
mean = df["value"].mean()
print("Pandas mean:", mean)
print("Czas:", time.time() - start)


start = time.time()
df = pl.read_csv(filename)
mean = df["value"].mean()
print("Polars mean:", mean)
print("Czas:", time.time() - start)


start = time.time()
df = pl.scan_csv(filename)

mean = df.select(pl.col("value").mean()).collect().item()
print("Polars lazy mean:", mean)
print("Czas:", time.time() - start)


start = time.time()
df = dd.read_csv(filename)

mean = df["value"].mean().compute()
print("Dask mean:", mean)
print("Czas:", time.time() - start)


