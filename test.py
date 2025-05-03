import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-180, 181, 1)
y = np.arange(-90, 91, 1)
X, Y = np.meshgrid(x, y)
u = -10*np.sin(2*np.pi*Y/180)*np.cos(np.pi*X/180)**2
v = 10*np.cos(np.pi*Y/180)**2*np.sin(2*np.pi*X/180)
ws = np.sqrt(u**2 + v**2)

zonally_ave = np.average(ws, 1)
plt.pcolormesh(X, Y, u)
plt.colorbar()
plt.title('u')
plt.show()
plt.close()
plt.pcolormesh(X, Y, v)
plt.colorbar()
plt.title('v')
plt.show()
plt.close()
plt.pcolormesh(X, Y, ws)
plt.colorbar()
plt.title('ws')
plt.show()
plt.close()