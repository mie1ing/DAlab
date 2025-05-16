import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def calculate_wind_speed(u_velocity, v_velocity):
    return np.sqrt(u_velocity ** 2 + v_velocity ** 2)


ds = xr.open_dataset('May2000-uvt.nc')
u = ds.u.sel(level=1000)
v = ds.v.sel(level=1000)

sur_wind_speed = calculate_wind_speed(u, v)
storm_mask = (sur_wind_speed > 20)

ds_storm = ds.where(storm_mask & (ds.level == 1000))

storm_count = np.sum(storm_mask.values, axis=(1, 2))

dates = ds_storm.time.values

readable_dates = [np.datetime_as_string(date, unit='D') for date in dates]

plt.figure(figsize=(12, 6))
plt.plot(readable_dates, storm_count, marker='o', linestyle='-', color='blue', linewidth=2)
plt.grid(True, linestyle='--', alpha=0.7)
plt.title('Number of Storm Locations as Function of Time', fontsize=16)
plt.xlabel('dates', fontsize=14)
plt.ylabel('Number of Storm Locations', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('storm_plots/daily_storm_count.png', bbox_inches='tight')
plt.close()

for day in dates:
    day_wind_speed = calculate_wind_speed(u.sel(time=day),
                                          v.sel(time=day)
                                          )

    day_storm_mask = storm_mask.sel(time=day)

    if not day_storm_mask.any():
        continue

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()

    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    cs_bg = day_wind_speed.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),
                                         cmap='Blues',
                                         add_colorbar=False
                                        )

    cs = day_wind_speed.where(day_storm_mask).plot.contour(ax=ax, colors='red',
                                                      transform=ccrs.PlateCarree(),
                                                      add_colorbar=False
                                                      )

    step = 3

    lons = u.sel(time=day).longitude.values
    lats = u.sel(time=day).latitude.values

    lon_subset = lons[::step]
    lat_subset = lats[::step]

    u_storm = u.sel(time=day).where(day_storm_mask)
    v_storm = v.sel(time=day).where(day_storm_mask)

    Q = ax.quiver(lon_subset, lat_subset,
                  u_storm.sel(longitude=lon_subset, latitude=lat_subset).values,
                  v_storm.sel(longitude=lon_subset, latitude=lat_subset).values,
                  scale=500,
                  color='red',
                  width=0.0025,
                  transform=ccrs.PlateCarree()
                  )

    qk = ax.quiverkey(Q, 0.8, 0.9,
                      20,
                      '20 m/s',
                      labelpos='E',
                      coordinates='figure'
                      )

    cbar = plt.colorbar(cs_bg, ax=ax, orientation='horizontal')
    cbar.set_label('Wind Speed (m/s)')

    day_str = np.datetime_as_string(day, unit='D')
    plt.title(f'Storm {day_str}', pad=20)

    plt.tight_layout()

    plt.savefig(f'storm_plots/lab4ex2_{day_str}.png', bbox_inches='tight')
    plt.close()

