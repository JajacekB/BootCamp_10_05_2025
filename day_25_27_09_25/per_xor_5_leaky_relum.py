import numpy as np


def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_derivative(x, alpha=0.01):
    return np.where(x > 0, 1, alpha)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [0], [0], [1]])

np.random.seed(42)

# W_hidden = np.random.rand(2, 2) * 2 - 1
# W_output = np.random.rand(2, 1) * 2 - 1

W_hidden = np.random.randn(2, 2) * np.sqrt(2/2)
W_output = np.random.randn(2, 1) * np.sqrt(2/2)

print(W_output.shape)

learning_rate = 0.1
epochs = 2000

for epoch in range(epochs):
    hidden_input = np.dot(X, W_hidden)
    hidden_output = leaky_relu(hidden_input)

    final_input = np.dot(hidden_output, W_output)
    final_output = leaky_relu(final_input)

    error = y - final_output

    d_output = error * leaky_relu_derivative(final_output)
    error_hidden = d_output.dot(W_output.T)
    d_hidden = error_hidden * leaky_relu_derivative(hidden_output)

    W_output += hidden_output.T.dot(d_output) * learning_rate
    W_hidden += X.T.dot(d_hidden) * learning_rate

for i in range(4):
    hidden_layer_input = np.dot(X[i], W_hidden)
    hidden_layer_output = leaky_relu(hidden_layer_input)

    final_input = np.dot(hidden_layer_output, W_output)
    final_output = leaky_relu(final_input)

    print(f"Wejście: {X[i]} -> Przewidywane wyjścia: {final_output[0]:.4f}")
    # print(f"Wejście: {X[i]} -> Przewidywane wyjścia: {(final_output[0] > 0.5):.4f}")
