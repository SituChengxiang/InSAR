# -*- coding: UTF-8 -*-
import laspy
from osgeo import osr
from osgeo import gdal
import numpy as np
import os

# 读取 las 文件
script_dir = os.path.dirname(os.path.abspath(__file__))
lasfile = os.path.join(script_dir, "ALS_LAI.las")
inFile = laspy.read(lasfile) 
# 获取点云坐标与属性
x, y, z = inFile.x, inFile.y, inFile.z
classfication = inFile.raw_classification
return_number = inFile.return_num
scan_angle = inFile.scan_angle_rank
# 读取对应的DEM数据
ds_dem = gdal.Open(os.path.join(script_dir, "sample_dem.tif"))
rows_dem = ds_dem.RasterYSize
cols_dem = ds_dem.RasterXSize
# 获取DEM栅格数据的原点和分辨率信息
transform = ds_dem.GetGeoTransform()
xOrigin_dem = transform[0]
yOrigin_dem = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]
# 计算每个点云对应的 DEM 栅格位置
xOffset_dem = ((x - xOrigin_dem) / pixelWidth).astype(int)
yOffset_dem = ((y - yOrigin_dem) / pixelHeight).astype(int)
# 确保索引在有效范围内
xOffset_dem = np.clip(xOffset_dem, 0, cols_dem - 1)
yOffset_dem = np.clip(yOffset_dem, 0, rows_dem - 1)
# 读取DEM数据并提取点云对应的高程
band = ds_dem.GetRasterBand(1)
dem_array = band.ReadAsArray()
point_dem = dem_array[yOffset_dem, xOffset_dem]
# 点云Z值归一化
normilze_z = z - point_dem
# 获取点云范围
x_max, y_max = inFile.header.max[0:2]
x_min, y_min = inFile.header.min[0:2]
# 设置生成LAI的分辨率
pixelwidth, pixelHeight = 10, -10
# 设置LAI栅格的原点和行列号
xOrigin = x_min
yOrigin = y_max
cols = int(round((x_max - x_min) / pixelwidth))
rows = int(round((y_max - y_min) / abs(pixelHeight)))
# 计算每个点云对应的LAI栅格位置
xOffset = ((x - xOrigin) / pixelwidth).astype(int)
yOffset = ((y - yOrigin) / pixelHeight).astype(int)
# 确保索引在有效范围内
xOffset = np.clip(xOffset, 0, cols - 1)
yOffset = np.clip(yOffset, 0, rows - 1)
# 设置存储孔隙率和LAI栅格的变量
gp = np.zeros((cols, rows))
lai = np.zeros((cols, rows))
# 计算每个LAI栅格的LAI值
for j in range(rows):
    for i in range(cols):
        # 获取当前栅格内的点云索引
        mask = (xOffset == i) & (yOffset == j)
        if np.sum(mask) == 0:
            gp[i, j] = 1.0
            lai[i, j] = 0.0
            continue
        # 计算高于2米的点数量
        vp = np.sum(mask & (normilze_z > 2))
        ttp = np.sum(mask)
        angles = np.mean(np.abs(scan_angle[mask]))
        gp[i, j] = 1 - float(vp) / float(ttp)
        lai[i, j] = -1 * np.cos(np.deg2rad(angles)) * np.log(gp[i, j] + 1e-6) / 0.5
# 输出成 geoTIFF
driver = gdal.GetDriverByName('GTiff')
outRaster = driver.Create('lai.tif', cols, rows, 1, gdal.GDT_Float32)
outRaster.SetGeoTransform((xOrigin, pixelwidth, 0, yOrigin, 0, pixelHeight))
outband = outRaster.GetRasterBand(1)
outband.WriteArray(np.transpose(lai))
# 设置投影信息
outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
outRaster.SetProjection(outRasterSRS.ExportToWkt())
outband.FlushCache()
outRaster = None