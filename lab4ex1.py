import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ds = xr.open_dataset('2000monthly-surft-prec.nc')
print(ds)
lsp = ds.lsp.isel(latitude=slice(19,29),longitude=slice(45,55))
t2m = ds.t2m.isel(latitude=slice(19,29),longitude=slice(45,55))
lsp_mean = lsp.mean(dim=['latitude','longitude'])
t2m_mean = t2m.mean(dim=['latitude','longitude'])
lsp_var = lsp.max(dim=['time']) - lsp.min(dim=['time'])
t2m_var = t2m.max(dim=['time']) - t2m.min(dim=['time'])
lsphz = lsp.sel(latitude=20.2, longitude=120.2, method='nearest')
t2mhz = t2m.sel(latitude=20.2, longitude=120.2, method='nearest')

fig = plt.figure(figsize=(10, 12))
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 2, 3)
ax4 = plt.subplot(2, 2, 4)

lsp_mean.plot(ax=ax1)
ax1.set_xlabel('time')
ax1.set_ylabel('average large-scale precipitation')

t2m_mean.plot(ax=ax2)
ax2.set_xlabel('time')
ax2.set_ylabel('average 2m temperature')

lsp_var.plot.pcolormesh(ax=ax3)

t2m_var.plot.pcolormesh(ax=ax4)

plt.tight_layout()

plt.show()
plt.close()