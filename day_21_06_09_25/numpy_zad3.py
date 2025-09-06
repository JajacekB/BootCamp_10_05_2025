import numpy as np

data = np.array(
    [
        [10, 15, 20],
        [25, 30, 35],
        [40, 45, 50],
        [55, 60, 65],
        [70, 75, 80]
    ]
)

print(data.ndim)

print(data[0])
print(data[1, 2])
print(data[3, 1])
