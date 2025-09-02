# -*- coding: UTF-8 -*-
import laspy
import numpy as np
from scipy import spatial
import open3d as o3d
import matplotlib
import matplotlib.pyplot as plt
import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

#las文件位置 示例数据为机载数据 但是算法通用
lasfile = os.path.join(script_dir, "sor.las")
#打开las文件
inFile = laspy.read(lasfile)
#读取激光雷达点云的xyz坐标
x,y,z = inFile.x,inFile.y,inFile.z
#点云显示
xyz_new = np.column_stack((x, y, z)).astype(np.float32)
pcd_new = o3d.geometry.PointCloud()
pcd_new.points = o3d.utility.Vector3dVector(xyz_new)
o3d.visualization.draw_geometries([pcd_new])
#封装x,y
lasdata = np.array(list(zip(x,y,z)))
tree = spatial.KDTree(lasdata)
#设置判断选择几倍SD作为阈值和领域点数
sigma=1  #SD
K=51     #领域点数
#建立每个点领域存储距离数组
k_dist=np.zeros_like(x)
#查找距离小于多少的点
for i in range(len(x)):
    dist,index =tree.query(np.array([x[i],y[i],z[i]]), K)
k_dist[i] = np.sum(dist)
#判断噪点的最大阈值
max_distance = np.mean(k_dist) + sigma*np.std(k_dist)
#去除噪点后的点云XYZ值
x=x[k_dist<max_distance]
y=y[k_dist<max_distance]
z=z[k_dist<max_distance]
print(x, y, z)
#噪点的索引
outer_index=np.where(k_dist>max_distance)
#噪声点显示成红色
pcd_new.paint_uniform_color([0.5, 0.5, 0.5])
np.asarray(pcd_new.colors)[outer_index, :] = [1, 0, 0]
o3d.visualization.draw_geometries([pcd_new])