import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from lab4ex2 import wind_velocity_quiver_plot as wvqp
from lab4ex2 import generate_plot_layout as gpl


def ave_wind_speed_profile_and_velocity(u_speed, v_speed):
    wind_speed = np.sqrt(u_speed ** 2 + v_speed ** 2)
    ave_wind_speed_profile = wind_speed.mean(dim='time')
    u_average = u_speed.mean(dim='time')
    v_average = v_speed.mean(dim='time')
    return ave_wind_speed_profile, u_average, v_average


def plot_wind_speed_and_velocity(wind_speed_profile, u_speed, v_speed, step):
    _, ax = gpl()

    cs_bg = wind_speed_profile.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),
                                         cmap='Blues',
                                         add_colorbar=False
                                     )

    Q, qk = wvqp(u_speed, v_speed, step, ax)

    cbar = plt.colorbar(cs_bg, ax=ax, orientation='horizontal')
    cbar.set_label('Wind Speed (m/s)')

    plt.show()


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


plot_wind_speed_and_velocity(ave_sur_wind_speed, u10_ave, v10_ave, 5)
plot_wind_speed_and_velocity(ave_top_trop_wind_speed, u_ave, v_ave, 5)