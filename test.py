import numpy as np
import matplotlib.pyplot as plt

pi=np.pi
x=np.linspace(0,pi,100)
y=np.linspace(0,2*pi,200)
(X,Y)=np.meshgrid(x,y)
Z=np.sin(X**2+Y)
ax=plt.axes(projection='3d')
surf=ax.plot_wireframe(X,Y,Z, rstride=5, cstride=10)
ax.view_init(69, 121) # changes the viewing angle
plt.show()