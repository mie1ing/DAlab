import xarray as xr
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats as st
import numpy as np

def hist_plot(u_data, target_latitude, north=True):
    if north:
        u_lat = u_data.sel(latitude=target_latitude).values.flatten()
    else:
        u_lat = u_data.sel(latitude=-target_latitude).values.flatten()

    hemisphere = 'N' if north else 'S'
    u_mean = u_lat.mean()
    u_std = u_lat.std()
    sns.histplot(u_lat)
    plt.title(f'u distribution at 500 hPa at {target_latitude}°{hemisphere}, mean = {u_mean:.2f}, std = {u_std:.2f}')
    plt.xlabel('u')
    plt.savefig(f'../67fe68e723632af9fad1411b/figures/lab6_7ex5_{target_latitude}_{hemisphere}.png')
    plt.close()

def student_t_test(u_data, target_latitude):
    u_north = u_data.sel(latitude=target_latitude).values.flatten()
    u_south = u_data.sel(latitude=-target_latitude).values.flatten()

    t_stat, p_val = st.ttest_ind(u_north, u_south)
    print(f't-statistic: {t_stat:.2f}, p-value: {p_val:.2f} at latitude: {target_latitude}°')

if __name__ == '__main__':
    ds = xr.open_dataset('../data/May2000-uvt.nc')

    u = ds['u'].sel(level=500)
    target_lat = 30

    # hist_plot(u, target_lat)
    # hist_plot(u, target_lat, north=False)
    student_t_test(u, target_lat)
