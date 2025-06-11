import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    ds = xr.open_dataset('../data/May2000-uvt.nc')
    u = ds['u'].sel(level=500)
    df = u.to_dataframe()
    df1 = df.reset_index(level=['latitude', 'time'])
    ax = plt.subplot(111)
    sns.boxplot(x='latitude', y='u', data=df1, ax=ax)
    for ind, label in enumerate(ax.get_xticklabels()):
        if ind % 6 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    plt.title('Boxplot of u at level 500')
    plt.savefig('../overleaf/67fe68e723632af9fad1411b/figures/lab6_7ex1.png')
