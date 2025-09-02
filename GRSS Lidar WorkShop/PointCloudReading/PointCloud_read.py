# -*- coding: UTF-8 -*-
import laspy
import numpy as np
import os
#las文件位置；“./”表示在当前工作路径下
script_dir = os.path.dirname(os.path.abspath(__file__))
lasfile = os.path.join(script_dir, "read.las")
#打开las文件
inFile = laspy.read(lasfile)
#读取激光雷达点云的xyz坐标
x, y, z = inFile. x, inFile. y, inFile. z
#读取点云分类信息
Classfication = inFile. raw_classification
#读取点云回波信息
return_num = inFile. return_num
#读取点云扫描角度信息
scan_angle_rank = inFile. scan_angle_rank
#点云数据构建索引
#KDtree索引使用了SciPy函数库中的spatial库
#KDtree原理可以参考本书第4.2节
#示例为根据水平坐标建立查找索引
from scipy import spatial
#封装x，y，如果建立三维索引，则需要封装x，y，z
lasdata = np.array(list(zip(x, y)))
#构建kd树索引
tree = spatial. KDTree(lasdata)
#查找中心点（323000，4102251）半径为1m圆内有多少点
aa = tree. query_ball_point(np. array([323000, 4102251]), 1)
#显示搜索到的x，y点云
print(x[aa], y[aa])
