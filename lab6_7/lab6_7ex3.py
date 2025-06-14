import xarray as xr
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

def sin_function(x, a, b, c, freq):
    return a + b * np.sin(freq * x + c)

def calculate_r2(y_true, y_pred):
    sse = np.sum((y_true - y_pred)**2)
    sst = np.sum((y_true - np.mean(y_true))**2)
    return 1 - sse/sst

def curfit_sin_function(dataset, selected_longitude):
    u = dataset['u'].sel(level=200, longitude=selected_longitude, method='nearest')

    u_true = u.sel(latitude=slice(15, -15)).mean(dim='latitude').values
    time = np.arange(len(u_true))
    (a, b, c, frequency), _ = opt.curve_fit(sin_function, time, u_true, p0=[0, 1, 0, 1])

    u_fitted = sin_function(time, a, b, c, frequency)
    r_squre = calculate_r2(u_true, u_fitted)

    return time, frequency, u_true, u_fitted, r_squre

def curfit_with_fixed_frequency(dataset, selected_longitude, fixed_frequency):
    u = dataset['u'].sel(level=200, longitude=selected_longitude, method='nearest')

    u_true = u.sel(latitude=slice(15, -15)).mean(dim='latitude').values
    time = np.arange(len(u_true))
    def fix_function(x, a1, b1, c1):
        return a1 + b1 * np.sin(fixed_frequency * x + c1)

    (a, b, c), _ = opt.curve_fit(fix_function, time, u_true, p0=[0, 1, 0])

    u_fitted = sin_function(time, a, b, c, fixed_frequency)
    r_squre = calculate_r2(u_true, u_fitted)

    return time, u_true, u_fitted, r_squre

def plot_fitting_result(time, y_true, y_pred, r_squre, selected_longitude):
    plt.plot(time, y_true, 'o', label='tropical u')
    plt.plot(time, y_pred, label='sin fit')
    plt.legend()
    plt.title(f'sin fit of tropical u (R² = {r_squre:.2f})')
    plt.xlabel('time')
    plt.ylabel('u')
    plt.savefig(f'../overleaf/67fe68e723632af9fad1411b/figures/lab6_7ex3_{selected_longitude}.png')
    plt.close()

if __name__ == '__main__':
    ds = xr.open_dataset('../data/May2000-uvt.nc')

    selected_lon = 180
    t, w, tropical_u, fitted_u, r2 = curfit_sin_function(ds, selected_lon)
    plot_fitting_result(t, tropical_u, fitted_u, r2, selected_lon)
    selected_lon = 160
    t, tropical_u, fitted_u, r2 = curfit_with_fixed_frequency(ds, selected_lon, w)
    plot_fitting_result(t, tropical_u, fitted_u, r2, selected_lon)
