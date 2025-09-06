import matplotlib.pyplot as plt
# pip install matplotlib
import numpy as np

y = np.linspace(0, 10, 100)  # dane z zakreso od 0 do 10 podzielone na 100 części
x = np.linspace(0, 10, 100)

plt.plot(x, y)

plt.xlabel("Oś X")
plt.ylabel("Oś Y")

plt.title("Wykres liniowy")
# plt.show()
# plt.savefig('wykres.png')
# plt.close()

# plt.savefig("wykres2.png", dpi=300)
# plt.close()

plt.savefig("wykres3", dpi=300, bbox_inches='tight')
plt.close()