import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# from lab4.lab4ex2 import generate_storm_dataset

ds = xr.open_dataset('data/May2000-uvt.nc')

# sds = generate_storm_dataset(ds)
#
# storm_counts = sds.groupby('time').count()
#
# storm_counts['u'].plot()
#
# plt.ylabel('storm count')
# plt.show()
# plt.close()

u = ds['u'].sel(level=1000)
v = ds['v'].sel(level=1000)
ws = np.sqrt(u ** 2 + v ** 2)
storm_mask = ws > 20

storm_count = storm_mask.sum(dim=['latitude', 'longitude'])
print(storm_count)

storm_count.plot()
plt.ylabel('storm count')
plt.show()
plt.close()