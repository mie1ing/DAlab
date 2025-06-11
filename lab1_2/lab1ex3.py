import numpy as np
import matplotlib.pyplot as plt

R = 2

t = np.linspace(-np.pi/2, np.pi/2, 100)
s = np.linspace(0, 2*np.pi, 100)

t, s = np.meshgrid(t, s)

X = R * np.cos(t) * np.cos(s)
Y = R * np.cos(t) * np.sin(s)
Z = R * np.sin(t)

ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, cmap='coolwarm')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Surface: $x^2 + y^2 + z^2 = 4$')
ax.set_box_aspect([1,1,1])
plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab1ex3.png')