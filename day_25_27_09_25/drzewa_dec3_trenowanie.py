import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree

X = np.array([
    [25, 30],
    [40, 70],
    [35, 50],
    [50, 90],
    [20, 20],
])

y = np.array([0, 1, 1, 1, 0])

