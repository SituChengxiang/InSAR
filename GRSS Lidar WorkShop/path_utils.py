# -*- coding: UTF-8 -*-
"""
通用路径处理工具
解决Python脚本在不同目录运行时的路径问题
"""
import os

def get_script_dir():
    """
    获取当前脚本所在的目录
    """
    return os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename):
    """
    获取数据文件的绝对路径
    Args:
        filename: 数据文件名
    Returns:
        数据文件的绝对路径
    """
    script_dir = get_script_dir()
    return os.path.join(script_dir, filename)

def get_output_path(filename):
    """
    获取输出文件的绝对路径
    Args:
        filename: 输出文件名
    Returns:
        输出文件的绝对路径
    """
    script_dir = get_script_dir()
    return os.path.join(script_dir, filename)

def setup_gdal():
    """
    设置GDAL异常处理，避免警告
    """
    try:
        from osgeo import gdal
        gdal.UseExceptions()
        print("GDAL异常处理已启用")
    except ImportError:
        print("GDAL未安装，跳过GDAL设置")

def ensure_dir_exists(file_path):
    """
    确保文件所在目录存在
    Args:
        file_path: 文件路径
    """
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"创建目录: {dir_path}")

# 使用示例
if __name__ == "__main__":
    print("脚本目录:", get_script_dir())
    print("数据文件路径:", get_data_path("example.las"))
    print("输出文件路径:", get_output_path("output.tif"))
