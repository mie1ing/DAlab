import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

def merging_data_sets(file_names):
    return xr.merge(
        [xr.open_dataset(filename) for filename in file_names]
    )


def globaly_average_plot(dataset, varname='varname'):
    variable = dataset[varname].mean(dim=['latitude', 'longitude'])
    dates = variable.time.values
    readable_dates = [np.datetime_as_string(date, unit='D') for date in dates]
    plt.plot(readable_dates, variable, linestyle='-', color='blue', linewidth=1)
    plt.title(f'Globaly average {varname}')
    plt.xlabel('dates')
    plt.ylabel(varname)

    every_nth = 12
    selected_dates = readable_dates[::every_nth]
    plt.xticks(selected_dates, selected_dates, rotation=45)

    ax = plt.gca()
    ax.grid(True, which='major', linestyle='--', alpha=0.7)
    ax.grid(False, which='minor')

    plt.tight_layout()
    plt.savefig(f'/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex4_2_{varname}.png')
    plt.close()

def zonally_average_contourf_plot(dataset, varname='varname', color='Blues'):
    variable = dataset[varname].mean(dim='longitude')
    cs = variable.plot.contourf(x='time', y='latitude', cmap=color, add_colorbar=False)

    ax = plt.gca()
    cbar = plt.colorbar(cs, ax=ax, orientation='horizontal')
    cbar.set_label(varname)
    plt.title(f'Zonally average {varname}')
    plt.xlabel('year')

    plt.savefig(f'/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex4_3_{varname}.png')
    plt.close()


if __name__ == "__main__":
    filenames = [f'1990s/{year}monthly-surft-prec.nc' for year in range(1990, 2001)]
    ds = merging_data_sets(filenames)
    ds.to_netcdf('1990s-2000s-monthly-surft-prec.nc')

    globaly_average_plot(ds, 'lsp')
    globaly_average_plot(ds, 't2m')
    zonally_average_contourf_plot(ds, 'lsp')
    zonally_average_contourf_plot(ds, 't2m', color='coolwarm')