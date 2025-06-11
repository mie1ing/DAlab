# This script uses a function from lab2ex2.py to calculate the wind energy spectra.

import numpy as np
import xarray as xr
from lab1_2.lab2ex2 import lab2_wind_speed as lab2_ws

ws, u, v, x, y = lab2_ws()
energy = 0.5 * (u**2 + v**2)
zonally_ave = np.average(energy, 1)
step = 2
energy_step = energy[::step, ::step]
exergy_ave_step = zonally_ave[::step]

ds = xr.Dataset({
    'u': xr.DataArray(u, dims=['Latitude', 'Longitude'],
                      coords={'Latitude': y, 'Longitude': x},
                      attrs={'units': 'm/s',
                             'long_name': 'meridional wind speed'}),
    'v': xr.DataArray(v, dims=['Latitude', 'Longitude'],
                      coords={'Latitude': y, 'Longitude': x},
                      attrs={'units': 'm/s',
                             'long_name': 'zonal wind speed'}),
    'E': xr.DataArray(energy_step, dims=['Latitude', 'Longitude'],
                      coords={'Latitude': y[::step], 'Longitude': x[::step]},
                      attrs={'units': 'm^2/s^2',
                             'long_name': 'kinetic energy density'}),
    'E_phi': xr.DataArray(exergy_ave_step, dims=['Latitude'],
                          coords={'Latitude': y[::step]},
                          attrs={'units': 'm^2/s^2',
                                 'long_name': 'zonally average of kinetic energy density'})
}, attrs={'title': 'Wind Energy Spectra'})

ds.to_netcdf('lab4ex6.nc')