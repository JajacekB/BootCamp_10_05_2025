import mnist
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from keras.datasets import mnist


def image_to_array(image_path: str, size: int=28) -> np.ndarray:
    image = Image.open(image_path).convert("L")
    image = ImageOps.invert(image)
    image = image.resize((size, size))
    image_array = np.array(image).astype(np.float32)
    image_array /= 255.0
    return image_array

# X * w + b
def transfor_linear(x: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    return x @ w + b

def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0)

def softmax(x:np.ndarray, axis: int = -1) -> np.ndarray:
    x -= np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)

def one_hot(y, num_classes = 10):
    return  np.eye(num_classes)[y]

dummy_x = np.arange(36).reshape(6, 6) - 18
print(dummy_x)
print(relu(dummy_x))

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_test.shape)
print(y_train.shape)

x_train = x_train.reshape(-1, 784).astype(np.float32) / 255.0
x_test = x_test.reshape(-1, 784).astype(np.float32) / 255.0
y_train_oh = one_hot(y_train)
y_test_oh = one_hot(y_test)

np.random.seed(42)
w1 = np.random.randn(784, 128) * 0.01
b1 = np.zeros((1, 128))
w2 = np.random.randn(128, 10) * 0.01
b2 = np.zeros((1, 10))

lr = 0.1
epochs = 5
batch_size = 64

print(f"Epoka {epoch + 1}, strata: {loss:.4f}")

x= x_test[0].reshape(1, -1)
y_true = y_test[0]

z1 = x @ w1 + b1
a1 = relu(z1)
z2 = a1 @ w2 + b2

y_pred = softmax(z2)

predicted_class = np.argmax(y_pred)

print("Prawdziwa cyfr:", y_true)
print("Sieć przewidziała:", predicted_class)
print("Porównanie", predicted_class == y_true)

plt.imshow(x_test[0].reshape(28, 28), cmap="gray")
pl.title



