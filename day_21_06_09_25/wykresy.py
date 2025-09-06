import matplotlib.pyplot as plt

import numpy as np
from matplotlib.patches import bbox_artist

y = np.linspace(0, 10, 100)
x = np.linspace(0, 10, 100)

plt.plot(x, y)

plt.xlabel("Oś X")
plt.ylabel("Oś Y")

plt.title("Wykres liniowy")
# plt.show()

plt.savefig('wykres.png')
plt.close()

plt.savefig('wykres2.png', dpi = 300)
plt.close()

plt.savefig('wykres3.png', dpi = 300, bbox_inches.size =3)
plt.close()




