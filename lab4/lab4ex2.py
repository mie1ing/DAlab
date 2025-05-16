import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def calculate_wind_speed(u_velocity, v_velocity):
    return np.sqrt(u_velocity ** 2 + v_velocity ** 2)


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


def generate_plot_layout():
    figure = plt.figure(figsize=(12, 8))
    axis = plt.axes(projection=ccrs.PlateCarree())
    axis.coastlines()

    gl = axis.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    return figure, axis


if __name__ == '__main__':
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

        _, ax = generate_plot_layout()

        cs_bg = day_wind_speed.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),
                                         cmap='Blues',
                                         add_colorbar=False
                                        )

        cs = day_wind_speed.where(day_storm_mask).plot.contour(ax=ax, colors='red',
                                                      transform=ccrs.PlateCarree(),
                                                      add_colorbar=False
                                                      )

        step = 3

        u_storm = u.sel(time=day).where(day_storm_mask)
        v_storm = v.sel(time=day).where(day_storm_mask)

        Q, qk = wind_velocity_quiver_plot(u_storm, v_storm, step, ax)

        cbar = plt.colorbar(cs_bg, ax=ax, orientation='horizontal')
        cbar.set_label('Wind Speed (m/s)')

        day_str = np.datetime_as_string(day, unit='D')
        plt.title(f'Storm {day_str}', pad=20)

        plt.tight_layout()

        plt.savefig(f'storm_plots/lab4ex2_{day_str}.png', bbox_inches='tight')
        plt.close()
