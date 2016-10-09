import numpy as np
import matplotlib.pyplot as plt

# make up some data in the interval ]0, 1[
x = np.arange(0, 1, 1/10000)
s_der = [(3 + np.cos(point)) for point in x]
z_der = [(4 - np.sin(point)) for point in x]
plt.plot(x, s_der, color='red')
plt.plot(x, z_der, color='green')
plt.show()