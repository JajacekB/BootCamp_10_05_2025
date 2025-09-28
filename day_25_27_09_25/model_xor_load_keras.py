import os
import numpy as np

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from tensorflow.keras.models import load_model

model = load_model("model_xor_02.keras")

model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

predictions = model.predict(X)
predictions = (predictions > 0.5).astype(int)

for i in range(len(X)):
    print(f"{X[i]} {predictions[i]}")