import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def generate_plot_layout():
    figure = plt.figure(figsize=(12, 8))
    axis = plt.axes(projection=ccrs.PlateCarree())
    axis.coastlines()

    gl = axis.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    return figure, axis


def generate_storm_dataset_and_mask(dataset):
    u = dataset['u'].sel(level=1000)
    v = dataset['v'].sel(level=1000)

    sws = np.sqrt(u ** 2 + v ** 2)
    storm_mask = sws > 20

    u_velocity_storm = u.where(storm_mask, drop=True)
    v_velocity_storm = v.where(storm_mask, drop=True)
    wind_speed_storm = sws.where(storm_mask, drop=True)

    dataset_for_strom = xr.Dataset({'u': u_velocity_storm,
                                'v': v_velocity_storm,
                                'ws': wind_speed_storm
                                    }).stack(points=("time", "latitude", "longitude"
                                                 )).dropna(dim="points")
    return dataset_for_strom, storm_mask


if __name__ == '__main__':
    ds = xr.open_dataset('May2000-uvt.nc')

    strom_dataset, mask = generate_storm_dataset_and_mask(ds)

    lons = strom_dataset['longitude'].values
    lats = strom_dataset['latitude'].values
    u_storm = strom_dataset['u'].values
    v_storm = strom_dataset['v'].values
    ws = strom_dataset['ws'].values

    _, ax = generate_plot_layout()
    cs = ax.scatter(lons, lats, c=ws, s=10, cmap='viridis')

    # Wind vector
    # qv = ax.quiver(lons, lats, u_storm, v_storm, color='red', scale=500, width=0.0025)
    # ax.quiverkey(qv, 0.9, 0.95, 20, '20 m/s', labelpos='E', coordinates='figure')

    cbar = plt.colorbar(cs, ax=ax, orientation='horizontal')
    cbar.set_label('Wind Speed (m/s)')
    plt.title('Storm Locations', fontsize=16)

    plt.tight_layout()

    plt.savefig('/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex2_1_quiver.png')
    plt.close()


    mask.sum(dim=['latitude', 'longitude']).plot(marker='o', linestyle='-', color='blue', linewidth=2)

    plt.xlabel('dates', fontsize=14)
    plt.ylabel('Number of Storm Locations', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title('Number of Storm Locations as Function of Time', fontsize=16)

    plt.tight_layout()

    plt.savefig('/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex2_2.png')
    plt.close()
