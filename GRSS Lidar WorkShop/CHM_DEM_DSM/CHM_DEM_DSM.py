##读取去噪后数据
import laspy
import numpy as np
from scipy import spatial
import pandas as pd
import open3d as o3d
import math
import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

#las文件位置 示例数据为机载数据 但是算法通用
lasfile = os.path.join(script_dir, 'ALS_small.las')
#打开las文件
inFile = laspy.read(lasfile)
#DEM
x,y,z = inFile.x,inFile.y,inFile.z
cls = inFile.classification
#提取边界
x_max,y_max = inFile.header.max[0:2]
x_min,y_min = inFile.header.min[0:2]
#分辨率
pixelWidth , pixelHeight = 1,-1
### calculate
xOrigin = x_min
yOrigin = y_max

cols = int(math.ceil(((x_max - x_min) / pixelWidth)))
rows = int(math.ceil(((y_max - y_min) / abs(pixelHeight))))

xOffset = (x - xOrigin) / pixelWidth
xOffset= xOffset.astype(int)
yOffset = (y - yOrigin) / pixelHeight
yOffset= yOffset.astype(int)
print(cols,rows)
x_index,y_index=np.meshgrid(np.arange(rows),np.arange(cols))
fill_value = np.full_like(x_index.flatten(),np.nan,dtype='double')
filled_points = np.column_stack([y_index.flatten(),x_index.flatten(),fill_value])
# for keep the exent consisited with las data
z_update = np.asarray(z, dtype=np.float64)

z_update[cls !=2] = np.nan
real_points = np.column_stack([xOffset,yOffset,z_update])
points = np.row_stack([real_points,filled_points])
pts = pd.DataFrame(points,columns=['Off_x','Off_y','z'])
min_raster=np.asarray(pts.pivot_table(index='Off_x',columns='Off_y',values='z',aggfunc='min',dropna=False))

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax = plt.subplot(111)
ax.imshow(np.transpose(np.array(min_raster)), interpolation=None, cmap='viridis')
plt.title("Digital Elevation Model")
fig.tight_layout()
plt.show()

# calculate the grid center distance
#x_index,y_index=np.meshgrid(np.arange(rows),np.arange(cols))
x_index=x_index.flatten()*pixelWidth + xOrigin
y_index=y_index.flatten()*pixelHeight + yOrigin
z_min_index=min_raster.flatten()
z_min_tmp = z_min_index
#封装x,y
griddata = np.array(list(zip(x_index,y_index)))
tree = spatial.cKDTree(griddata)
#领域点数
K=200
#查找空值点
nan_index= np.where(np.isnan(z_min_tmp))
dist,index =tree.query(griddata[nan_index], K)
###去除查询的网格中心点
dist=dist[:,1:K-1]
index=index[:,1:K-1]
#计算权重
w = 1.0 / dist**2
#筛除NAN值
w_nan_index= np.where(np.isnan(z_min_tmp[index]))
w[w_nan_index]=0
z_idw = np.nansum(w * z_min_tmp[index], axis=1) / np.sum(w, axis=1)
z_min_tmp[nan_index]=z_idw

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax = plt.subplot(111)
ax.imshow(np.transpose(np.array(z_min_tmp.reshape(cols,rows))), interpolation=None, cmap='viridis')
plt.title("Digital Elevation Model after applying IDW")
fig.tight_layout()
plt.show()

#DSM
x,y,z = inFile.x,inFile.y,inFile.z
return_number = inFile.return_num
# for keep the exent consisited with las data
z_update = np.asarray(z, dtype=np.float64)
z_update[return_number != 1 ] = np.nan
real_points = np.column_stack([xOffset,yOffset,z_update])
points = np.row_stack([real_points,filled_points])
pts = pd.DataFrame(points,columns=['Off_x','Off_y','z'])
max_raster=np.asarray(pts.pivot_table(index='Off_x',columns='Off_y',values='z',aggfunc='max',dropna=False))

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax = plt.subplot(111)
# ax.imshow(np.transpose(np.array(max_raster)), interpolation=None, cmap='viridis')
# plt.title("Digital Surface Model")
# fig.tight_layout()
# plt.show()

x_index,y_index=np.meshgrid(np.arange(rows),np.arange(cols))
x_index=x_index.flatten()*pixelWidth + xOrigin
y_index=y_index.flatten()*pixelHeight + yOrigin
z_max_index=max_raster.flatten()
z_max_tmp = z_max_index
#封装x,y
griddata = np.array(list(zip(x_index,y_index)))
tree = spatial.cKDTree(griddata)
#领域点数
K=200
#查找空值点
nan_index= np.where(np.isnan(z_max_tmp))
dist,index =tree.query(griddata[nan_index], K)
###去除查询的网格中心点
dist=dist[:,1:K-1]
index=index[:,1:K-1]
#计算权重
w = 1.0 / dist**2
#筛除NAN值
w_nan_index= np.where(np.isnan(z_max_tmp[index]))
w[w_nan_index]=0
z_idw = np.nansum(w * z_max_tmp[index], axis=1) / np.sum(w, axis=1)
z_max_tmp[nan_index]=z_idw

# import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax = plt.subplot(111)
ax.imshow(np.transpose(np.array(z_max_tmp.reshape(cols,rows))), interpolation=None, cmap='viridis')
plt.title("Digital Surface Model after applying IDW")
fig.tight_layout()
plt.show()

#CHM
chm_raster=z_max_tmp.reshape(cols,rows)-z_min_tmp.reshape(cols,rows)

fig, ax = plt.subplots()
ax = plt.subplot(111)
ax.imshow(np.transpose(chm_raster), interpolation=None, cmap='viridis')
plt.title("Canopy Height Model")
fig.tight_layout()
plt.show()


from osgeo import osr
from osgeo import gdal

# 设置GDAL异常处理，避免警告
gdal.UseExceptions()
#输出成geoTIFF
driver = gdal.GetDriverByName('GTiff')
outRaster = driver.Create(os.path.join(script_dir, 'DEM.tif'), cols, rows, 1, gdal.GDT_Float32)
outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))
outband = outRaster.GetRasterBand(1)
#flip arrary
outband.WriteArray(np.transpose(z_min_tmp.reshape(cols,rows)))
outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
outRaster.SetProjection(outRasterSRS.ExportToWkt())
outband.FlushCache()
outRaster = None

#输出成geoTIFF
driver = gdal.GetDriverByName('GTiff')
outRaster = driver.Create(os.path.join(script_dir, 'DSM.tif'), cols, rows, 1, gdal.GDT_Float32)
outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))
outband = outRaster.GetRasterBand(1)
#flip arrary
outband.WriteArray(np.transpose(z_max_tmp.reshape(cols,rows)))
outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
outRaster.SetProjection(outRasterSRS.ExportToWkt())
outband.FlushCache()
outRaster = None

#输出成geoTIFF
driver = gdal.GetDriverByName('GTiff')
outRaster = driver.Create(os.path.join(script_dir, 'CHM.tif'), cols, rows, 1, gdal.GDT_Float32)
outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))
outband = outRaster.GetRasterBand(1)
#flip arrary
outband.WriteArray(np.transpose(chm_raster))
outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
outRaster.SetProjection(outRasterSRS.ExportToWkt())
outband.FlushCache()
outRaster = None