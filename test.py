from scipy.fftpack import diff as psdiff
import numpy as np
import matplotlib.pyplot as plt

pi=np.pi; L=50; N=1000; Nc=50; fs=N/(2*L)

x=np.linspace(0,L,N, endpoint=False)
u=np.cos(2*pi*x/25)
uxan=-2*pi/25*np.sin(2*pi*x/25)
ux = psdiff(u, period=L)
plt.plot(x,u, label="u")
plt.plot(x,ux, label="du/dx")
plt.plot(x,uxan-ux,label="Difference to analytic")
plt.legend()
plt.show()
plt.close()