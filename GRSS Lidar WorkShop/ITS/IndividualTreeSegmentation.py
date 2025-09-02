# -*- coding: UTF-8 -*-
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy.ndimage import gaussian_filter
import os
#读取冠层高度模型CHM
script_dir = os.path.dirname(os.path.abspath(__file__))
raster = gdal.Open(os.path.join(script_dir, "chm.tif"))
banddataraster = raster.GetRasterBand(1)
dataraster = banddataraster.ReadAsArray()
# 对CHM进行高斯滤波，平滑数据
dataraster_gau = gaussian_filter(dataraster, sigma=1)
# 寻找CHM中的局部最大值作为分水岭的标记点
coordinates = peak_local_max(dataraster_gau, min_distance=1)
local_maxi = np.zeros_like(dataraster_gau, dtype=bool)
local_maxi[tuple(coordinates.T)] = True
markers = ndi.label(local_maxi)[0]
# 利用分水岭算法进行分割，labels变量中存储了每个分割结果
labels = watershed(-dataraster_gau, markers, mask= dataraster_gau[:]>5)
# 利用matplotlib出图查看初步结果
fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box'})
ax = axes.ravel()
# 绘制CHM
ax[0].imshow(-dataraster, cmap=plt.get_cmap("Spectral"))
ax[0].set_title('CHM')
# 绘制高斯滤波后的CHM
ax[1].imshow(dataraster_gau, cmap=plt.get_cmap("Spectral"))
ax[1].set_title('CHM_gs')
# 绘制分割结果
ax[2].imshow(labels, cmap=plt.get_cmap("Spectral"))
ax[2].set_title('Segment')
for a in ax:
    a.set_axis_off()
fig.tight_layout()
plt.show()