import numpy as np
import matplotlib.pyplot as plt

def lab2_wind_speed():
    x = np.arange(-180, 181, 1)
    y = np.arange(-90, 91, 1)
    X, Y = np.meshgrid(x, y)
    u = -10*np.sin(2*np.pi*Y/180)*np.cos(np.pi*X/180)**2
    v = 10*np.cos(np.pi*Y/180)**2*np.sin(2*np.pi*X/180)
    windspeed = np.sqrt(u**2 + v**2)
    return windspeed, u, v, x, y


if __name__ == "__main__":
    ws, u, v, x, y = lab2_wind_speed()
    zonally_ave = np.average(ws, 1)
    plt.plot(y, zonally_ave)
    plt.xlim(-90, 90)
    plt.xticks(np.arange(-90, 91, 30))
    plt.ylabel('Zonally Averaged Wind Speed')
    plt.xlabel('Latitude')
    plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab2ex2.png')