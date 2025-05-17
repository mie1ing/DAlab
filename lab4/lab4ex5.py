import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def zonally_average_plot(dataset, varname='varname'):
    variable = dataset[varname].mean(dim='longitude')
    seasons = ['DJF', 'MAM', 'JJA', 'SON']
    for season in seasons:
        plt.plot(variable.latitude,
                 variable.sel(season=season),
                 linestyle='-', linewidth=1, label=season)

    plt.title(f'Seasonal zonally average {varname}')
    plt.xlabel('latitude')
    plt.ylabel(varname)
    plt.grid(linestyle='--', alpha=0.7)

    plt.legend()
    plt.savefig(f'/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex5_1_{varname}.png')
    plt.close()


def seasonal_varibility_plot(dataset, varname='varname', color='Blues'):
    varibility = dataset.groupby('season').max(dim='time') - dataset.groupby('season').min(dim='time')
    g = varibility[varname].plot.contourf(x='longitude', y='latitude',
                                          col='season', col_wrap=2, cmap=color,
                                          subplot_kws={'projection': ccrs.PlateCarree()})
    g.map(lambda: plt.gca().coastlines(linewidth=0.25))
    g.fig.suptitle(f'Seasonal varibility of {varname}')

    plt.savefig(f'/Users/bigmizhou/PycharmProjects/DAlab/overleaf/67fe68e723632af9fad1411b/figures/lab4ex5_2_{varname}.png')
    plt.close()


if __name__ == '__main__':
    ds = xr.open_dataset('2000monthly-surft-prec.nc')

    season_dict = {1: 'DJF', 2: 'DJF', 3: 'MAM', 4: 'MAM', 5: 'MAM',
                   6: 'JJA', 7: 'JJA', 8: 'JJA', 9: 'SON', 10: 'SON',
                   11: 'SON', 12: 'DJF'}
    ds = ds.assign_coords(season=("time", [season_dict[t.dt.month.item()] for t in ds.time]))

    seasonal_means = ds.groupby("season").mean(dim='time')

    zonally_average_plot(seasonal_means, 't2m')
    zonally_average_plot(seasonal_means, 'lsp')
    seasonal_varibility_plot(ds, 't2m', color='coolwarm')
    seasonal_varibility_plot(ds, 'lsp')