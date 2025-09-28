import os
import time
import numpy as np

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
from tensorflow import keras
from keras import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import platform
import cpuinfo



print(platform.processor())
# print(cpuinfo.get_cpu_info()['flags'])

print("Dostepne urzadzenia:")
print(tf.config.list_logical_devices())

# input()
# dane wejściowe
X = np.array(
    [[0, 0],
     [0, 1],
     [1, 0],
     [1, 1]]
)

# dane do nauki
y_xor = np.array([[0], [1], [1], [0]])
y_and = np.array([[0], [0], [0], [1]])
y_or = np.array([[0], [1], [1], [1]])

def train_model(y_train, logic_type):
    print(f"Uczenie modelu dla operacji: {logic_type}")

    model = Sequential([
        Input(shape=(2, )),
        Dense(4, activation="relu",),
        Dense(1, activation="sigmoid",)
    ])

    model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])

    with tf.device("/GPU:0"):
        model.fit(X, y_train, epochs=700, verbose=1)

    predictions = model.predict(X)
    predictions = (predictions > 0.5).astype(int)

    print(f"Przewidywanie wyników dla operacji: {logic_type}")
    for i in range(len(X)):
        print(f"{X[i]} {predictions[i][0]} oczekuje: {y_train[i][0]}")

    return  model

start_time = time.time()

model_xor = train_model(y_xor, "XOR")

print(f'Estimated time:{time.time() - start_time}')

model_xor.save("model_xor_03.keras")
print("Model został zapisany")

weights = model_xor.get_weights()
filename = "weights_only_03.npz"
np.savez(filename, *weights)
print("Wagi zostały zapisane")