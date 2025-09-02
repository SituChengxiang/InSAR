# -*- coding: UTF-8 -*-
import laspy
import numpy as np
import pandas as pd
from scipy import ndimage
import matplotlib.pyplot as plt
import os

#las文件位置
script_dir = os.path.dirname(os.path.abspath(__file__))
lasfile = os.path.join(script_dir, "filter.las")
#打开las文件
inFile = laspy.read(lasfile)
#获取点云坐标
x,y,z = inFile.x,inFile.y,inFile.z
cls = inFile.classification
#获取点云数据范围
xmin,xmax=min(x),max(x)
ymin,ymax=min(y),max(y)
#rasterize
#设置分辨率 0.5m * 0.5mpandas
pixelWidth,pixelHeight=0.5,-0.5
nrow=int(np.ceil(abs((ymax-ymin)/pixelHeight)))
ncol=int(np.ceil(abs((xmax-xmin)/pixelWidth)))
#设置初始网格
int_dem_mask = np.zeros((ncol,nrow),dtype='float')
int_dem_mask[:,:] = -9999.0
#设置网格起始点
xOrigin = xmin
yOrigin = ymax
#计算点云在网格的位置
xOffset = (x - xOrigin) / pixelWidth
xOffset = xOffset.astype(int)
yOffset = (y - yOrigin) / pixelHeight
yOffset = yOffset.astype(int)
#统计网格最低点
points = np.column_stack([xOffset,yOffset,z])
pts = pd.DataFrame(points,columns=['Off_x','Off_y','z'])
min_raster=np.asarray(pts.pivot_table(columns='Off_y',index='Off_x',values='z',aggfunc='min'))
#将邻近点赋值给网格空值
index = np.where(np.isnan(min_raster))
for i in range(len(index[0])):
    ix,iy=index[0][i],index[1][i]
    #查找领域数据，如未搜索到数据，继续按步长2增长搜索数据
    Fill_Flag = True
    win_size = 1
    while Fill_Flag:
        win_size = 1 + 2
        x_index = list(range(int(ix-(win_size-1)/2), int(ix+(win_size-1)/2+1)))*win_size
        y_index = np.repeat(list(range(int(iy-(win_size-1)/2), int(iy+(win_size-1)/2+1))),win_size)
        #去除网格外点，避免程序出错
        mask_x =  ((np.asarray(x_index)<0) | (np.asarray(x_index)>ncol -1))
        mask_y =  ((np.asarray(y_index)<0) | (np.asarray(y_index)>nrow -1))
        win_mask = mask_x + mask_y
        x_idx = np.asarray(x_index)[~win_mask]
        y_idx = np.asarray(y_index)[~win_mask]
        # 使用 np.ix_ 构造二维索引
        win_data = min_raster[np.ix_(x_idx, y_idx)]
        #去除数据空值NaN
        win_data = win_data[~np.isnan(win_data)]
        if len(win_data) !=0:
            min_raster[ix,iy]= win_data[0]
            min_raster[ix,iy]= np.mean(win_data)
            Fill_Flag = False
#设置高差参数
dh_max,dh0 = 1,0.1
#设置坡度提升
s=0.7
#复制初始栅格
pts_cls = np.zeros_like(z)
#设置形态学滤波的窗口迭代次数
for k in range(1,16):
    #设置初始窗体大小
    b=1 #线性增长
    wk = 2*k*b+1
    #开运算
    tmp_raster = ndimage.grey_opening(min_raster,size=(wk,wk))
    #根据窗体大小计算高差
    if wk <= 3:
        dh = dh0
    else:
        wk_l = 2*(k-1)*b+1
        dh = s*(wk-wk_l)*pixelWidth + dh0
    if dh > dh_max:
        dh=dh_max
    #标记地面点
    for i_row in range(nrow):
        for i_col in range(ncol):
            #获取网格对应点云的索引
            cls_index = np.where((points[:,0]==i_col) & (points[:,1]==i_row))[0]
            #判断距离阈值
            dh_index = np.where((points[cls_index,2]-tmp_raster[i_col,i_row]) > dh)
            if len(dh_index[0])>0:
                pts_cls[cls_index[dh_index]]=1
                #显示每次迭代后的地面点数量
                print('Ground points:' + str(len(np.where(pts_cls[:]==0)[0])))
# 最后pts_cls变量存储了哪些点为地面点和非地面点信息
print(pts_cls)
from mpl_toolkits.mplot3d import Axes3D
ax = plt.subplot(111,projection='3d')
ax.scatter(x,y,z,c=pts_cls,marker='.',s=4,linewidth=0,alpha=0.9)
plt.show()
exit(0)