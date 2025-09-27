import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [0], [0], [1]])

np.random.seed(42)

W_hidden = np.random.rand(2, 2)
W_output = np.random.rand(2, 1)

learning_rate = 0.5
epochs = 5000

for epoch in range(epochs):
    hidden_input = np.dot(X, W_hidden)
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, W_output)
    output = sigmoid(output_input)

    error = y - output
    d_output = error * (output *(1 - output))
    error_hidden = d_output.dot(W_output.T)
    d_hidden = error_hidden *(hidden_output * (1 - hidden_output))

    W_output += hidden_output.T.dot(d_output) * learning_rate
    W_hidden += X.T.dot(d_hidden) * learning_rate

for i in range(4):
    hidden_input = np.dot(X[i], W_hidden)
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, W_output)
    output = sigmoid(output_input)

