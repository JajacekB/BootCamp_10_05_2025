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

# trenowanie drzewa
tree = DecisionTreeClassifier(criterion='gini', max_depth=2)
tree.fit(X, y)

decision = tree.predict(np.array([[30, 40]]))
print("Pozyczka przyznana" if decision[0] == 1 else "Pozyczka odrzucona")

plt.figure(figsize=(8,5))
plot_tree(tree, feature_names=["wiek", "zarobki"],
          class_names=['odrzucona', 'przyznana'], filled=True
          )
plt.title("Drzewo decyzyjne pozyczki")
plt.tight_layout()
plt.show()