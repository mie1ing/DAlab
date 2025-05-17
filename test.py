# import xarray as xr
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
#
# ds = xr.open_dataset('lab4/2000monthly-surft-prec.nc')
#
# season_dict = {1: 'DJF', 2: 'DJF', 3: 'MAM', 4: 'MAM', 5: 'MAM',
#                6: 'JJA', 7: 'JJA', 8: 'JJA', 9: 'SON', 10: 'SON',
#                11: 'SON', 12: 'DJF'}
# ds = ds.assign_coords(season=("time", [season_dict[t.dt.month.item()] for t in ds.time]))
#
# seasonal_means = ds.groupby("season").mean(dim='time')


# zonally_average_lsp = seasonal_means['lsp'].mean(dim='longitude')
#
# seasons = ['DJF', 'MAM', 'JJA', 'SON']
#
# for season in seasons:
#     plt.plot(zonally_average_lsp.latitude,
#              zonally_average_lsp.sel(season=season),
#              linestyle='-', linewidth=1, label=season)
#
# plt.title('Seasonal zonally average large-scale precipitation')
# plt.xlabel('latitude')
# plt.ylabel('zonally average lsp')
#
# plt.legend()
# plt.show()


# varibility = ds.groupby('season').max(dim='time') - ds.groupby('season').min(dim='time')
#
# g = varibility['lsp'].plot.contourf(x='longitude', y='latitude',
#                                 col='season', col_wrap=2, cmap='Blues',
#                                 subplot_kws={'projection': ccrs.PlateCarree()})
# g.map(lambda: plt.gca().coastlines(linewidth=0.25))
#
# plt.show()
# plt.close()