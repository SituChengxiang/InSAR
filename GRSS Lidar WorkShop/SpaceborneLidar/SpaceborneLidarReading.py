# -*- coding: UTF-8 -*-
import h5py
import numpy as np
import os
#设置GLAS01和GLAS14文件
script_dir = os.path.dirname(os.path.abspath(__file__))
HDF_list_GLA14=os.path.join(script_dir, "GLAH14_DATA.H5")
HDF_list_GLA01=os.path.join(script_dir, "GLAH01_DATA.H5")
#读取GLAS14文件
f_GLA14 = h5py.File(HDF_list_GLA14,'r')
#读取GLAS14中的激光发射记录标号，生成唯一表示ID
recNdx=f_GLA14['Data_40HZ']['Time']['i_rec_ndx']
shotNum=f_GLA14['Data_40HZ']['Time']['i_shot_count']
GLA14_ID=recNdx[:]*100.0+shotNum
#读取GLAS14中记录的经纬度信息
lat_dataset = f_GLA14['Data_40HZ']['Geolocation']['d_lat']
lon_dataset = f_GLA14['Data_40HZ']['Geolocation']['d_lon']
#计算GLAS波形参数中的RH100
d_SigBegOff = f_GLA14['Data_40HZ']['Elevation_Offsets']['d_SigBegOff']
d_gpCntRngOff = f_GLA14['Data_40HZ']['Elevation_Offsets']['d_gpCntRngOff']
RH100_all=d_gpCntRngOff[:,0]-d_SigBegOff
#读取GLAS01文件
GLA01 = h5py.File(HDF_list_GLA01,'r')
#读取GLAS01中的激光发射记录标号，生成唯一表示ID
f_01_recNdx=GLA01['Data_40HZ']['Time']['i_rec_ndx']
f_01_shotNum=GLA01['Data_40HZ']['Time']['i_shot_count']
GLA01_ID=f_01_recNdx[:]*100.0+f_01_shotNum
#匹配GLAS14和GLAS01中的编号并生成掩膜数据
mask_14 = np.in1d(GLA14_ID, GLA01_ID)
if np.sum(mask_14)==0:
    print("no match...")
    exit(99)
mask_01 = np.in1d(GLA01_ID, GLA14_ID)
#匹配GLAS14和GLAS01中的编号并生成掩膜数据
f_01_rec_wf=GLA01['Data_40HZ']['Waveform']['RecWaveform']['r_rng_wf']
f_01_rec_wf=np.asarray(f_01_rec_wf)
#读取GLAS01中的波形类型、波形信号起始位置、波形信号终止位置
waveformType = GLA01['Data_40HZ']['Waveform']['Characteristics']['i_waveformType']
#读取GLAS01中波形信号终止位置
trailingEdge = GLA01['Data_40HZ']['Waveform']['Characteristics']['i_LastThrXingT']
#读取GLAS01中的波形信号起始位置
leadingEdge = GLA01['Data_40HZ']['Waveform']['Characteristics']['i_NextThrXing']
#计算波形宽度
waveformExtent = (trailingEdge[:]-leadingEdge[:])*299792458.0/1000000000.0
#读取GLAS01中的波形数据
waveformRec = GLA01['Data_40HZ']['Waveform']['RecWaveform']['r_rng_wf']
#读取GLAS01中的每束激光的记录位置、能量和时间
recWfLocationIndex = GLA01['Data_40HZ']['Waveform']['RecWaveform']['i_rec_wf_location_index']
recWfLocationTable = GLA01['ANCILLARY_DATA'].attrs['rec_wf_sample_location_table']
RespEndTime = GLA01['Data_40HZ']['Waveform']['RecWaveform']['i_RespEndTime']
#根据波形能量判断第一个次和最后一次出现最高能量一半的位置
countShot = 0
firstHalfAmp = np.empty_like(waveformType, dtype=np.float32)
lastHalfAmp = np.empty_like(waveformType, dtype=np.float32)
# waveformType[:]==0
firstHalfAmp[:] = -9999  #-9999代表缺省值
lastHalfAmp[:] = -9999
for waveformRow in waveformRec:
    if waveformType[countShot] == 0:
        firstHalfAmp[countShot] = -9999
        lastHalfAmp[countShot] = -9999
        continue
    elif waveformType[countShot] == 1:
        index = np.where(waveformRow[:] >= (np.max(waveformRow[:])/2))
        if np.size(index[0]) > 0:
            firstHalfAmp[countShot] = RespEndTime[countShot] + recWfLocationTable[recWfLocationIndex[countShot]-1, index[0][-1]]
            lastHalfAmp[countShot] = RespEndTime[countShot] + recWfLocationTable[recWfLocationIndex[countShot]-1,index[0][0]]
        else:
            firstHalfAmp[countShot] = -9999
            lastHalfAmp[countShot] = -9999
    else:
        index = np.where(waveformRow[0:200] >= (np.max(waveformRow[0:200])/2))
        if np.size(index[0]) > 0:
            firstHalfAmp[countShot] = RespEndTime[countShot] + recWfLocationTable[recWfLocationIndex[countShot]-1, index[0][-1]]
            lastHalfAmp[countShot] = RespEndTime[countShot] + recWfLocationTable[recWfLocationIndex[countShot]-1, index[0][0]]
        else:
            firstHalfAmp[countShot] = -9999
            lastHalfAmp[countShot] = -9999
    countShot += 1
#计算波形前沿长度
leadingEdgeExtent = (firstHalfAmp[:] - leadingEdge[:])*299792458.0/1000000000.0
#计算波形后沿长度
trailingEdgeExtent = (trailingEdge[:] - lastHalfAmp[:])*299792458.0/1000000000.0
#去除异常数据
index_mask = np.where(firstHalfAmp == -9999)
leadingEdgeExtent[index_mask] = -9999
trailingEdgeExtent[index_mask] = -9999
#利用掩膜数据过滤结果,去除不匹配的点
we = waveformExtent[mask_01]/2.0
lee =leadingEdgeExtent[mask_01]/2.0
tee =trailingEdgeExtent[mask_01]/2.0
#关闭打开的GLAS文件
GLA01.close()
f_GLA14.close()