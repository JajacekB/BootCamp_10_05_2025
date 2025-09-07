import numpy as np


initial_value = 10000
years = 10
annual_return = 0.07
annual_volatility = 0.15
simulation = 1000

np.random.seed(42)

annual_growth_rates = np.random.normal(annual_return, annual_volatility, (years, simulation))

values = initial_value * np.cumprod(1 + annual_growth_rates, axis=0)

final_values = values[-1]

print("Średnia wartość portfela po 10 latach:", np.mean(final_values))
print("Najlepszy sczenarisz:", np.max(final_values))
print("Najgorszy sczenarisz:", np.min(final_values))