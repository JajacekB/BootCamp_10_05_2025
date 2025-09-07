# import mnist
import os

from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


def image_to_array(image_path: str, size: int = 28) -> np.ndarray:
    image = Image.open(image_path).convert("L")  # L - odcienie szarosci
    image = ImageOps.invert(image)
    image = image.resize((size, size))
    image_array = np.array(image).astype(np.float32)
    image_array /= 255.0
    return image_array


# Perceptron wielowarstwowy
# trzy warzztwy neuronów
# X * w + b
def transfor_linear(x: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    return x @ w + b  # @ to samo co dot, mnożenie macierzowe


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0)


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x -= np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def one_hot(y, num_classes=10):
    return np.eye(num_classes)[y]


def relu_derivative(x):
    return (x > 0).astype(np.float32)


# Funkcja strat
def cross_entropy(predictions, labels):
    return -np.mean(np.sum(labels * np.log(predictions + 1e-8), axis=1))


dummy_x = np.arange(36).reshape(6, 6) - 18
print(dummy_x)
print(relu(dummy_x))

# wczytanie danych MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_test.shape)  # (10000, 28, 28)
print(y_train.shape)  # (60000,)

x_train = x_train.reshape(-1, 784).astype(np.float32) / 255.0
x_test = x_test.reshape(-1, 784).astype(np.float32) / 255.0
y_train_oh = one_hot(y_train)
y_test_oh = one_hot(y_test)

# inicjalizacja wag
# np.random.seed(42)
w1 = np.random.randn(784, 128) * 0.01
b1 = np.zeros((1, 128))
w2 = np.random.randn(128, 10) * 0.01
b2 = np.zeros((1, 10))

# parametry treningu
lr = 0.1
epochs = 10
batch_size = 64

# Trening
for epoch in range(epochs):
    for i in range(0, len(x_train), batch_size):
        x_batch = x_train[i:i + batch_size]
        y_batch = y_train_oh[i:i + batch_size]

        # Forward pass
        z1 = x_batch @ w1 + b1
        a1 = relu(z1)
        z2 = a1 @ w2 + b2
        y_pred = softmax(z2)

        # Loss
        loss = cross_entropy(y_pred, y_batch)

        # Backpropagation
        dz2 = y_pred - y_batch
        dw2 = a1.T @ dz2 / batch_size
        db2 = np.sum(dz2, axis=0, keepdims=True) / batch_size

        da1 = dz2 @ w2.T
        dz1 = da1 * relu_derivative(z1)
        dw1 = x_batch.T @ dz1 / batch_size
        db1 = np.sum(dz1, axis=0, keepdims=True) / batch_size

        # Aktualizacja wag
        w1 -= lr * dw1
        b1 -= lr * db1
        w2 -= lr * dw2
        b2 -= lr * db2

    print(f"Epoka {epoch + 1}, strata: {loss:.4f}")

# testowanie jedej próbki
# x = x_test[0].reshape(1, -1)
# y_true = y_test[0]
idx = np.random.randint(0, len(x_test))
x = x_test[idx].reshape(1, -1)
y_true = y_test[idx]

# przewidywanie sieci
z1 = x @ w1 + b1
a1 = relu(z1)
z2 = a1 @ w2 + b2

y_pred = softmax(z2)

predicted_class = np.argmax(y_pred)

print("PRawdziwa cyfra:", y_true)
print("Sieć przewidziała:", predicted_class)
print("Porównanie:", predicted_class == y_true)
# PRawdziwa cyfra: 7
# Sieć przewidziała: 7
# Porównanie: True

# plt.imshow(x_test[0].reshape(28, 28), cmap="gray")
plt.imshow(x_test[idx].reshape(28, 28), cmap="gray")
plt.title(f"Prawda: {y_true}, Przewidziana: {predicted_class}")
plt.axis('off')
plt.show()
