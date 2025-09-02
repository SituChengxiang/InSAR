# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import os
# 读取点云数据 (修复分隔符问题)
script_dir = os.path.dirname(os.path.abspath(__file__))
data = np.loadtxt(open(os.path.join(script_dir, "TLS_LAI.txt"), "rb"), delimiter=None, usecols=(0, 1, 2), dtype=float, skiprows=1)
# 设置体素大小
voxel_size = [0.003, 0.003, 0.003]
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
# 获得坐标范围
xmin, xmax = np.min(x), np.max(x)
ymin, ymax = np.min(y), np.max(y)
zmin, zmax = np.min(z), np.max(z)
# 体素尺寸 (更清晰的命名)
voxel_width = voxel_size[0]   # X方向
voxel_length = voxel_size[1]  # Y方向
voxel_height = voxel_size[2]  # Z方向
# 计算体素索引
xOffset = np.ceil((x - xmin) / voxel_width)
yOffset = np.ceil((y - ymin) / voxel_length)
zOffset = np.ceil((z - zmin) / voxel_height)
# 计算各维度体素数量 
num_cols = np.ceil((xmax - xmin) / voxel_width) 
num_rows = np.ceil((ymax - ymin) / voxel_length)
num_heights = np.ceil((zmax - zmin) / voxel_height)
# 每层体素总数
voxels_per_layer = num_rows * num_cols
# 组合偏移量并去重
points = np.column_stack([xOffset, yOffset, zOffset])
unique_voxels = np.unique(points, axis=0)
# 按Z分层统计
voxel_df = pd.DataFrame(unique_voxels, columns=['x_idx', 'y_idx', 'z_idx'])
grouped = voxel_df.groupby('z_idx')
# 计算每层填充率
layer_density = grouped.size() / voxels_per_layer
# 计算LAI
LAI = np.sum(layer_density) * 1.1
print("计算得到的LAI值为:", LAI)