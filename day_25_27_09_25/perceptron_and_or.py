import numpy as np

def signoid(x):
    return 1 / (1 + np.exp(-x))

def signoid_derivative(x):
    return x * (1 - x)

X = np.array([[0,0], [0,1], [1, 0], [1, 1]])
y = np.array([
    [0, 0],
    [0, 1],
    [0, 1],
    [1, 1]
])

# np.random.seed(42)
W = np.random.rand(2, 2) * 2 - 1
bias = np.random.rand(2) * 2 - 1

learning_rate = 0.1
epochs = 500

for epoch in range(epochs):
    weighed_sum = np.dot(X, W) + bias
    output = signoid(weighed_sum)

    error = y - output

    delta = error * signoid_derivative(output)

    W += np.dot(X.T, delta) * learning_rate
    bias += np.sum(delta, axis=0) * learning_rate

for i in range(4):
    wynik = signoid(np.dot(X[i], W) + bias)
    print(f"Wejsćie: {X[i]} -> AND: {wynik[0]:4f}, OR: {wynik[1]:4f}")
    print(f"Wejsćie: {X[i]} -> AND: {int(wynik[0] > 0.5)}, OR: {int(wynik[1] > 0.5)}")
