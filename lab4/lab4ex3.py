# This script uses functions from lab4ex2.py

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from lab4ex2 import generate_plot_layout as gpl

def wind_velocity_quiver_plot(u_velocity, v_velocity, subset_step, axis):
    longitude_subset = u_velocity.longitude.values[::subset_step]
    latitude_subset = v_velocity.latitude.values[::subset_step]

    qv = axis.quiver(longitude_subset, latitude_subset,
                  u_velocity.sel(longitude=longitude_subset, latitude=latitude_subset).values,
                  v_velocity.sel(longitude=longitude_subset, latitude=latitude_subset).values,
                  scale=500,
                  color='red',
                  width=0.0025,
                  transform=ccrs.PlateCarree()
                  )

    Qkey = axis.quiverkey(qv, 0.9, 0.95,
                      20,
                      '20 m/s',
                      labelpos='E',
                      coordinates='figure'
                      )
    return qv, Qkey


def ave_wind_speed_profile_and_velocity(u_speed, v_speed):
    wind_speed = np.sqrt(u_speed ** 2 + v_speed ** 2)
    ave_wind_speed_profile = wind_speed.mean(dim='time')
    u_average = u_speed.mean(dim='time')
    v_average = v_speed.mean(dim='time')
    return ave_wind_speed_profile, u_average, v_average


def plot_wind_speed_and_velocity(wind_speed_profile, u_speed, v_speed, step, filename=None):
    _, ax = gpl()

    cs_bg = wind_speed_profile.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),
                                         cmap='Blues',
                                         add_colorbar=False
                                     )

    Q, qk = wind_velocity_quiver_plot(u_speed, v_speed, step, ax)

    cbar = plt.colorbar(cs_bg, ax=ax, orientation='horizontal')
    cbar.set_label('Wind Speed (m/s)')

    plt.title(f'{filename} average wind and wind speed', pad=20)
    plt.tight_layout()

    plt.savefig(f'/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex3_1_{filename}.png')
    plt.close()


if __name__ == '__main__':
    # surface wind speed data
    ds = xr.open_dataset('may2000-surf.nc')
    u10 = ds.u10
    v10 = ds.v10
    ds.close()
    ave_sur_wind_speed, u10_ave, v10_ave = ave_wind_speed_profile_and_velocity(u10, v10)

    # top of tropopause wind speed data
    ds = xr.open_dataset('May2000-uvt.nc')
    u = ds.u.sel(level=200, method='nearest')
    v = ds.v.sel(level=200, method='nearest')
    ds.close()
    ave_top_trop_wind_speed, u_ave, v_ave = ave_wind_speed_profile_and_velocity(u, v)
    wspeed = np.sqrt(ds.u ** 2 + ds.v ** 2)
    ds['wspeed'] = wspeed
    ds.to_netcdf('May2000-uvt_wspeed.nc')

    plot_wind_speed_and_velocity(ave_sur_wind_speed, u10_ave, v10_ave, 5, 'surface')
    plot_wind_speed_and_velocity(ave_top_trop_wind_speed, u_ave, v_ave, 5, 'tropopause')