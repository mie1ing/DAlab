# import xarray as xr
# import cartopy.crs as ccrs
# import matplotlib.pyplot as plt
# from lab4.lab4ex2 import generate_plot_layout as gpl
# from lab4.lab4ex3 import wind_velocity_quiver_plot, ave_wind_speed_profile_and_velocity
#
#
# if __name__ == '__main__':
#     ds = xr.open_dataset('data/May2000-uvt.nc')
#     u = ds['u'].sel(level=1000, latitude=slice(15, -15))
#     v = ds['v'].sel(level=1000, latitude=slice(15, -15))
#     ds.close()
#     correlation = xr.corr(u, v, dim='time')
#
#     _, u_ave, v_ave = ave_wind_speed_profile_and_velocity(u, v)
#
#     _, ax = gpl()
#
#     im = correlation.plot(ax=ax, transform=ccrs.PlateCarree(),
#                           cmap='RdBu_r', vmin=-1, vmax=1,
#                           add_colorbar=False
#                           )
#     cbar = plt.colorbar(im, ax=ax, orientation='horizontal')
#     cbar.set_label('Correlation Coefficient')
#
#     Q, qk = wind_velocity_quiver_plot(u_ave, v_ave, subset_step=5, axis=ax)
#
#     plt.title('Correlation between the surface zonal and meridional wind')
#     plt.tight_layout()
#     plt.show()
#     plt.close()
