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


def generate_storm_dataset(dataset):
    u = dataset['u'].sel(level=1000)
    v = dataset['v'].sel(level=1000)

    sws = calculate_wind_speed(u, v)
    storm_mask = sws > 20

    u_velocity_storm = u.where(storm_mask, drop=True)
    v_velocity_storm = v.where(storm_mask, drop=True)
    wind_speed_storm = sws.where(storm_mask, drop=True)

    dataset_for_strom = xr.Dataset({'u': u_velocity_storm,
                                'v': v_velocity_storm,
                                'ws': wind_speed_storm
                                    }).stack(points=("time", "latitude", "longitude"
                                                 )).dropna(dim="points")
    return dataset_for_strom


if __name__ == '__main__':
    ds = xr.open_dataset('May2000-uvt.nc')

    strom_dataset = generate_storm_dataset(ds)

    lons = strom_dataset['longitude'].values
    lats = strom_dataset['latitude'].values
    u_storm = strom_dataset['u'].values
    v_storm = strom_dataset['v'].values
    ws = strom_dataset['ws'].values

    _, ax = generate_plot_layout()
    cs = ax.scatter(lons, lats, c=ws, s=10, cmap='viridis')

    # ax.quiver(lons, lats, u_storm, v_storm, color='red', scale=500, width=0.0025)

    cbar = plt.colorbar(cs, ax=ax, orientation='horizontal')
    cbar.set_label('Wind Speed (m/s)')
    plt.title('Storm Locations', fontsize=16)
    plt.tight_layout()
    plt.show()
    plt.close()
    #
    # ds_storm = ds.where(storm_mask & (ds.level == 1000))
    #
    # storm_count = np.sum(storm_mask.values, axis=(1, 2))
    #
    # dates = ds_storm.time.values
    #
    # readable_dates = [np.datetime_as_string(date, unit='D') for date in dates]
    #
    # plt.figure(figsize=(12, 6))
    # plt.plot(readable_dates, storm_count, marker='o', linestyle='-', color='blue', linewidth=2)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.title('Number of Storm Locations as Function of Time', fontsize=16)
    # plt.xlabel('dates', fontsize=14)
    # plt.ylabel('Number of Storm Locations', fontsize=14)
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    #
    # plt.savefig('storm_plots/daily_storm_count.png', bbox_inches='tight')
    # plt.close()
    #
