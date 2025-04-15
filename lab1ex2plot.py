import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelmax

file = open("kdvt.dat","rb")
t = np.load(file)
file.close()

file = open("kdvx.dat","rb")
x = np.load(file)
file.close()

file = open("kdvsol.dat","rb")
sol = np.load(file)
file.close()

X, Y = np.meshgrid(x, t)
plt.pcolormesh(X, Y, sol)
plt.colorbar()
plt.xlabel('x')
plt.ylabel('t')
plt.title('Korteveg de Vries on a Periodic Domain')
plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab1ex2.png')
plt.close()

crests_start = argrelmax(sol[0,:])
crests_end = argrelmax(sol[-1,:])

phase_speed = (x[crests_end[0][0]] - x[crests_start[0][0]]) / (t[-1] - t[0])
print(f'Phase Speed: {phase_speed}')