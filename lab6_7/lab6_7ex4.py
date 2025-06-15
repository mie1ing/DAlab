import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score, mean_squared_error

def linear_regression_two(x1, x2, z):
    Xt = np.concatenate((x1[:, np.newaxis], x2[:, np.newaxis]), axis=1)
    regr = linear_model.LinearRegression()
    regr.fit(Xt, z)
    return regr.predict(Xt), r2_score(z, regr.predict(Xt)), regr.coef_, regr.intercept_

def linear_regression_three(x1, x2, x3, z):
    Xt = np.concatenate((x1[:,np.newaxis], x2[:,np.newaxis], x3[:,np.newaxis]), axis=1)
    regr = linear_model.LinearRegression()
    regr.fit(Xt, z)
    return regr.predict(Xt), r2_score(z, regr.predict(Xt)), regr.coef_, regr.intercept_

def linear_fit_around_point(u, t, target_latitude, target_longitude, use_three_points=False):
    lat_idx = np.abs(t.latitude - target_latitude).argmin().item()
    lon_idx = np.abs(t.longitude - target_longitude).argmin().item()

    u_center = u.isel(longitude=lon_idx, latitude=lat_idx).values

    if lon_idx == 0:
        t_left = t.isel(longitude=len(surf_tropic_t.longitude) - 1, latitude=lat_idx).values
        t_right = t.isel(longitude=lon_idx + 1, latitude=lat_idx).values
    elif lon_idx == len(surf_tropic_t.longitude) - 1:
        t_left = t.isel(longitude=lon_idx - 1, latitude=lat_idx).values
        t_right = t.isel(longitude=0, latitude=lat_idx).values
    else:
        t_left = t.isel(longitude=lon_idx - 1, latitude=lat_idx).values
        t_right = t.isel(longitude=lon_idx + 1, latitude=lat_idx).values

    if use_three_points:
        t_center = t.isel(longitude=lon_idx, latitude=lat_idx).values
        fitted, r_square, coefficients, intercept = linear_regression_three(t_left, t_center, t_right, u_center)
    else:
        fitted, r_square, coefficients, intercept = linear_regression_two(t_left, t_right, u_center)

    return fitted, r_square, coefficients, intercept

def find_max_r2(latitude, longitudes):
    all_r2_2 = []
    all_r2_3 = []

    for lon in longitudes:
        _, r2_2, _, _ = linear_fit_around_point(surf_tropic_u, surf_tropic_t, latitude, lon, use_three_points=False)
        _, r2_3, _, _ = linear_fit_around_point(surf_tropic_u, surf_tropic_t, latitude, lon, use_three_points=True)
        all_r2_2.append(r2_2)
        all_r2_3.append(r2_3)

    max_r2_index = all_r2_2.index(max(all_r2_2))
    max_r2_index_2 = all_r2_3.index(max(all_r2_3))
    print(f"The maximum r2 is {max(all_r2_2)} with longitude {longitudes[max_r2_index]} for 2 points fit")
    print(f"The maximum r2 is {max(all_r2_3)} with longitude {longitudes[max_r2_index_2]} for 3 points fit")
    return all_r2_2, all_r2_3

if __name__ == '__main__':
    ds = xr.open_dataset('../data/May2000-uvt.nc')

    surf_tropic_u = ds['u'].sel(level=1000, latitude=slice(15, -15))
    surf_tropic_t = ds['t'].sel(level=1000, latitude=slice(15, -15))

    target_lat = 0
    target_lon = 265

    z, r2, fit_coef, interception = linear_fit_around_point(surf_tropic_u, surf_tropic_t, target_lat, target_lon)
    time_values = surf_tropic_t['time']

    plt.scatter(time_values, surf_tropic_u.sel(longitude=265, latitude=0), label='u')
    plt.plot(time_values, z, label='fit', color='red')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('u')
    plt.xticks(rotation=45)
    plt.title(f'Linear fit around tropical point at {target_lat}°N, {target_lon}°E, R² = {r2:.2f}')
    plt.grid()
    plt.savefig('../overleaf/67fe68e723632af9fad1411b/figures/lab6_7ex4_1.png')
    plt.close()

    all_r2_lon, all_r2_2_lon = find_max_r2(0, surf_tropic_u.longitude.values)

    plt.plot(surf_tropic_t.longitude, all_r2_lon, label='2 points fit')
    plt.plot(surf_tropic_t.longitude, all_r2_2_lon, label='3 points fit')
    plt.legend()
    plt.xlabel('longitude')
    plt.ylabel('r2')
    plt.title('R² of linear fit around tropical point at eqator')
    plt.ylim(0, 1)
    plt.grid()
    plt.savefig('../overleaf/67fe68e723632af9fad1411b/figures/lab6_7ex4_2.png')
    plt.close()

    another_lat = 0
    another_lon = 70

    another_u = surf_tropic_u.sel(longitude=another_lon, latitude=another_lat)

    lat_idx = np.abs(surf_tropic_t.latitude - another_lat).argmin().item()
    lon_idx = np.abs(surf_tropic_t.longitude - another_lon).argmin().item()

    t_left = surf_tropic_t.isel(longitude=lon_idx - 1, latitude=lat_idx).values
    t_right = surf_tropic_t.isel(longitude=0, latitude=lat_idx).values

    apply_fitting = t_left * fit_coef[0] + t_right * fit_coef[1] + interception
    another_r2 = r2_score(another_u, apply_fitting)
    MSE = mean_squared_error(another_u, apply_fitting)

    plt.plot(time_values, apply_fitting, label='fit', color='red')
    plt.scatter(time_values, another_u, label='u')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('u')
    plt.xticks(rotation=45)
    plt.title(f'Apply fitting model on point at {another_lat}°N, {another_lon}°E, R² = {another_r2:.2f}, MSE = {MSE:.2f}')
    plt.grid()
    plt.savefig('../67fe68e723632af9fad1411b/figures/lab6_7ex4_3.png')
    plt.close()

