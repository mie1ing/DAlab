import xarray as xr
import seaborn as sns
from matplotlib import pyplot as plt

def hist_plot(u_data, target_latitude, north=True):
    if north:
        u_lat = u_data.sel(latitude=target_latitude).values.flatten()
    else:
        u_lat = u_data.sel(latitude=-target_latitude).values.flatten()

    hemisphere = 'N' if north else 'S'
    sns.histplot(u_lat)
    plt.title(f'u distribution at 500 hPa at {target_latitude}°{hemisphere}')
    plt.xlabel('u')
    plt.show()
    plt.close()

if __name__ == '__main__':
    ds = xr.open_dataset('../data/May2000-uvt.nc')

    u = ds['u'].sel(level=500)
    target_lat = 30

    hist_plot(u, target_lat)
    hist_plot(u, target_lat, north=False)