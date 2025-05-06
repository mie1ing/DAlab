import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

ds = xr.open_dataset('2000monthly-surft-prec.nc')
lsp = ds.lsp.isel(latitude=slice(18,29),longitude=slice(44,55))
t2m = ds.t2m.isel(latitude=slice(18,29),longitude=slice(44,55))
time_values = lsp.time.values
lsp_mean = lsp.mean(dim=['latitude','longitude'])
t2m_mean = t2m.mean(dim=['latitude','longitude'])
lsp_var = lsp.max(dim=['time']) - lsp.min(dim=['time'])
t2m_var = t2m.max(dim=['time']) - t2m.min(dim=['time'])
lsphz = lsp.sel(latitude=20.2, longitude=120.2, method='nearest').values
t2mhz = t2m.sel(latitude=20.2, longitude=120.2, method='nearest').values

warmest_month = t2m_mean.argmax(dim='time')
driest_month = lsp_mean.argmin(dim='time')

warmest_month_time = time_values[warmest_month.values]
driest_month_time = time_values[driest_month.values]

warmest_month_formatted = pd.to_datetime(warmest_month_time).strftime('%B')
driest_month_formatted = pd.to_datetime(driest_month_time).strftime('%B')

print(f'The warmest month is {warmest_month_formatted}')
print(f'The driest month is {driest_month_formatted}')

fig = plt.figure(figsize=(12, 12))
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 2, 3, projection=ccrs.PlateCarree())
ax4 = plt.subplot(2, 2, 4, projection=ccrs.PlateCarree())

lsp_mean.plot(ax=ax1)
ax1.set_xlabel('time')
ax1.set_ylabel('average large-scale precipitation')

t2m_mean.plot(ax=ax2)
ax2.set_xlabel('time')
ax2.set_ylabel('average 2m temperature')

city_lon, city_lat = 120.2, 30.2
city_name = 'Hangzhou'

def setup_map(ax, var_data, city_longitude, city_latitude, city):
    ax.set_extent([110, 135, 20, 45])
    var_data.plot(ax=ax, transform=ccrs.PlateCarree())
    ax.coastlines(resolution='50m', linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.gridlines(draw_labels=True)
    ax.plot(city_longitude, city_latitude, 'ro', markersize=8, transform=ccrs.PlateCarree())
    ax.text(city_longitude + 0.3, city_latitude + 0.3, city, transform=ccrs.PlateCarree(),
            horizontalalignment='center', verticalalignment='center', fontsize=10)


setup_map(ax3, lsp_var, city_lon, city_lat, city_name)
ax3.set_title('large-scale precipitation variation')
setup_map(ax4, t2m_var, city_lon, city_lat, city_name)
ax4.set_title('2m temperature variation')

plt.tight_layout()

plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab4ex1_1.png')
plt.show()
plt.close()

plt.scatter(t2mhz, lsphz)
plt.xlabel('2m temperature')
plt.ylabel('large-scale precipitation')
plt.title('2m temperature v large-scale precipitation at Hangzhou')
plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab4ex1_2.png')
plt.show()
plt.close()