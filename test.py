import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd

if __name__ == '__main__':
    ds = xr.open_dataset('data/May2000-uvt.nc')

    surf_tropic_u = ds['u'].sel(level=1000, latitude=slice(15, -15))
    surf_tropic_t = ds['t'].sel(level=1000, latitude=slice(15, -15))

    # 在热带地区选择一个点（例如：纬度0度，经度120度）
    # 找到最接近的网格点索引
    target_lat = 0
    target_lon = 120

    # 找到最接近目标位置的索引
    lat_idx = np.abs(surf_tropic_t.latitude - target_lat).argmin().item()
    lon_idx = np.abs(surf_tropic_t.longitude - target_lon).argmin().item()

    print(f"选择的点: 纬度 {surf_tropic_t.latitude[lat_idx].values:.2f}°, "
          f"经度 {surf_tropic_t.longitude[lon_idx].values:.2f}°")
    print(f"索引: i={lon_idx}, j={lat_idx}")

    # 准备预测变量和目标变量
    # 预测变量：ti-1,j 和 ti+1,j （相邻经度的温度）
    # 目标变量：ui,j （当前点的风速）

    # 确保我们有足够的经度点来获取相邻点
    if lon_idx > 0 and lon_idx < len(surf_tropic_t.longitude) - 1:
        # 获取时间维度的所有数据
        t_left = surf_tropic_t.isel(longitude=lon_idx - 1, latitude=lat_idx)  # ti-1,j
        t_right = surf_tropic_t.isel(longitude=lon_idx + 1, latitude=lat_idx)  # ti+1,j
        u_center = surf_tropic_u.isel(longitude=lon_idx, latitude=lat_idx)  # ui,j

        # 转换为numpy数组并移除NaN值
        t_left_values = t_left.values
        t_right_values = t_right.values
        u_center_values = u_center.values

        # 创建预测变量矩阵 (温度梯度的代理变量)
        X = np.column_stack([t_left_values, t_right_values])
        y = u_center_values

        # 移除包含NaN的行
        valid_mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
        X_clean = X[valid_mask]
        y_clean = y[valid_mask]

        print(f"有效数据点数量: {len(X_clean)}")

        if len(X_clean) > 0:
            # 构建线性回归模型
            model = LinearRegression()
            model.fit(X_clean, y_clean)

            # 进行预测
            y_pred = model.predict(X_clean)

            # 计算模型性能
            r2 = r2_score(y_clean, y_pred)

            print(f"\n线性回归结果:")
            print(f"截距: {model.intercept_:.4f}")
            print(f"系数: {model.coef_}")
            print(f"  - t(i-1,j)的系数: {model.coef_[0]:.4f}")
            print(f"  - t(i+1,j)的系数: {model.coef_[1]:.4f}")
            print(f"R² 得分: {r2:.4f}")

            # 计算温度梯度 (ti+1,j - ti-1,j) / (2 * Δlon)
            lon_spacing = float(surf_tropic_t.longitude[1] - surf_tropic_t.longitude[0])
            temp_gradient = (t_right_values[valid_mask] - t_left_values[valid_mask]) / (2 * lon_spacing)

            # 创建可视化
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))

            # 1. 实际值 vs 预测值
            axes[0, 0].scatter(y_clean, y_pred, alpha=0.6)
            axes[0, 0].plot([y_clean.min(), y_clean.max()], [y_clean.min(), y_clean.max()], 'r--', lw=2)
            axes[0, 0].set_xlabel('实际风速 (m/s)')
            axes[0, 0].set_ylabel('预测风速 (m/s)')
            axes[0, 0].set_title(f'实际值 vs 预测值 (R² = {r2:.3f})')
            axes[0, 0].grid(True, alpha=0.3)

            # 2. 残差图
            residuals = y_clean - y_pred
            axes[0, 1].scatter(y_pred, residuals, alpha=0.6)
            axes[0, 1].axhline(y=0, color='r', linestyle='--')
            axes[0, 1].set_xlabel('预测风速 (m/s)')
            axes[0, 1].set_ylabel('残差 (m/s)')
            axes[0, 1].set_title('残差图')
            axes[0, 1].grid(True, alpha=0.3)

            # 3. 温度梯度 vs 风速
            axes[1, 0].scatter(temp_gradient, y_clean, alpha=0.6, color='green')
            axes[1, 0].set_xlabel('温度梯度 (K/degree)')
            axes[1, 0].set_ylabel('风速 (m/s)')
            axes[1, 0].set_title('温度梯度 vs 风速')
            axes[1, 0].grid(True, alpha=0.3)

            # 4. 时间序列
            time_values = surf_tropic_u.time[valid_mask]
            axes[1, 1].plot(time_values, y_clean, 'b-', label='实际值', alpha=0.7)
            axes[1, 1].plot(time_values, y_pred, 'r-', label='预测值', alpha=0.7)
            axes[1, 1].set_xlabel('时间')
            axes[1, 1].set_ylabel('风速 (m/s)')
            axes[1, 1].set_title('时间序列对比')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()

            # 打印一些统计信息
            print(f"\n统计信息:")
            print(f"实际风速: 均值={np.mean(y_clean):.3f}, 标准差={np.std(y_clean):.3f}")
            print(f"预测风速: 均值={np.mean(y_pred):.3f}, 标准差={np.std(y_pred):.3f}")
            print(f"残差: 均值={np.mean(residuals):.3f}, 标准差={np.std(residuals):.3f}")
            print(f"温度梯度: 均值={np.mean(temp_gradient):.6f}, 标准差={np.std(temp_gradient):.6f}")

        else:
            print("错误: 没有有效的数据点进行建模")
    else:
        print("错误: 选择的经度索引无法获取相邻点，请选择其他点")
