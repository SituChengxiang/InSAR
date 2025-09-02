# -*- coding: UTF-8 -*-
import laspy
from osgeo import osr
from osgeo import gdal
import numpy as np
import os
# 读取 las 文件
script_dir = os.path.dirname(os.path.abspath(__file__))
lasfile = os.path.join(script_dir, "canopycover.las")
inFile = laspy.read(lasfile) 
# 获取点云坐标和属性信息
x, y, z = inFile.x, inFile.y, inFile.z
classification = inFile.classification
return_number = inFile.return_num
# 读取点云对应的DEM数据
ds_dem = gdal.Open(os.path.join(script_dir, "sample_dem.tif"))
rows = ds_dem.RasterYSize
cols_dem = ds_dem.RasterXSize
bands = ds_dem.RasterCount
# 获取DEM栅格数据的原点和分辨率信息
transform = ds_dem.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]
# 计算每个点云对应的DEM栅格位置
xOffset = ((x - xOrigin) / pixelWidth).astype(int)
yOffset = ((y - yOrigin) / pixelHeight).astype(int)
# 读取DEM数据
band = ds_dem.GetRasterBand(1)
bandArray = band.ReadAsArray()
# 获取点云对应的DEM值
point_dem = bandArray[yOffset, xOffset]
# 点云的值归一化
normalized_z = z - point_dem  # 修正变量名拼写
# 获取点云范围
x_min, y_min, _ = inFile.header.mins
x_max, y_max, _ = inFile.header.maxs
# 设置生成冠盖度的分辨率
cc_pixelWidth, cc_pixelHeight = 10, -10
# 设置冠盖度栅格的原点和行列号
xOrigin_cc = x_min
yOrigin_cc = y_max
cols_cc = int(round((x_max - x_min) / cc_pixelWidth))
rows_cc = int(round((y_max - y_min) / abs(cc_pixelHeight))) 
# 计算每个点云对应的冠盖度栅格位置
xOffset_cc = ((x - xOrigin_cc) / cc_pixelWidth).astype(int)
yOffset_cc = ((y - yOrigin_cc) / cc_pixelHeight).astype(int)
# 创建存储冠盖度栅格的数组
cc = np.zeros((rows_cc, cols_cc))
# 计算每个栅格的冠盖度
for i in range(cols_cc):
    for j in range(rows_cc):
        # 获取当前栅格内的点云索引
        mask = (xOffset_cc == i) & (yOffset_cc == j) & (return_number == 1)
        # 有效点总数 (第一回波)
        ttp = np.sum(mask)
        if ttp > 0:
            # 植被点数 (归一化高度>2m的第一回波)
            vp = np.sum(mask & (normalized_z > 2))
            cc[j, i] = float(vp) / float(ttp)
# 输出成geoTIFF
driver = gdal.GetDriverByName('GTiff')
outRaster = driver.Create('canopy_cover.tif', cols_cc, rows_cc, 1, gdal.GDT_Float32)
outRaster.SetGeoTransform((xOrigin_cc, cc_pixelWidth, 0, yOrigin_cc, 0, cc_pixelHeight))
# 设置投影信息
outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
outRaster.SetProjection(outRasterSRS.ExportToWkt())
outband = outRaster.GetRasterBand(1)
outband.WriteArray(cc)
outband.FlushCache()
outRaster = None