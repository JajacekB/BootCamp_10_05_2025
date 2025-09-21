import polars as pl
import numpy as np
import os

rows_per_chunk = 1_000_000
total_rows = 2_000_000
filename = "bigfile_polars.csv"
categories = np.array(['A', 'B', 'C', 'D'])
np.random.seed(42)

if os.path.exists(filename):
    os.remove(filename)

for i, start in enumerate(range(0, total_rows, rows_per_chunk)):
    end = min(start + rows_per_chunk, total_rows)
    n_rows = end - start
    data = {
        "value": np.random.randint(0, 10_000, size=n_rows),
        "category": np.random.choice(categories, size=n_rows)
    }

    df = pl.DataFrame(data)
    if i == 0:
        df.write_csv(filename)
    else:
        with open(filename, "a", encoding="utf-8") as f:
            df.write_csv(f, include_header=False)
        print(f"Zapisano wiersze {start} - {end}")

    print("Zrobone!")