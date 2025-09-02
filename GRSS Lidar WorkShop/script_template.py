# -*- coding: UTF-8 -*-
"""
LiDAR数据处理脚本模板
通用路径处理方案，解决在不同目录运行时的路径问题
"""

import os
import sys

# =============================================================================
# 通用路径处理函数
# =============================================================================

def get_script_dir():
    """获取当前脚本所在的目录"""
    return os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename):
    """获取数据文件的绝对路径"""
    return os.path.join(get_script_dir(), filename)

def get_output_path(filename):
    """获取输出文件的绝对路径"""
    return os.path.join(get_script_dir(), filename)

def setup_environment():
    """设置运行环境"""
    # 添加脚本目录到Python路径
    script_dir = get_script_dir()
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # 设置GDAL（如果需要）
    try:
        from osgeo import gdal
        gdal.UseExceptions()
        print("✓ GDAL异常处理已启用")
    except ImportError:
        print("⚠ GDAL未安装")
    
    print(f"✓ 脚本目录: {script_dir}")

# =============================================================================
# 主要处理代码
# =============================================================================

def main():
    """主处理函数"""
    # 设置环境
    setup_environment()
    
    # 导入必要的库
    try:
        import laspy
        import numpy as np
        import matplotlib.pyplot as plt
        # 添加其他需要的库
        print("✓ 所有库导入成功")
    except ImportError as e:
        print(f"✗ 库导入失败: {e}")
        return
    
    # 设置数据文件路径
    las_file = get_data_path("your_data_file.las")  # 修改为你的数据文件名
    
    # 检查文件是否存在
    if not os.path.exists(las_file):
        print(f"✗ 数据文件不存在: {las_file}")
        return
    
    print(f"✓ 数据文件: {las_file}")
    
    # =========================================================================
    # 在这里添加你的数据处理代码
    # =========================================================================
    
    # 示例：读取LAS文件
    # inFile = laspy.read(las_file)
    # x, y, z = inFile.x, inFile.y, inFile.z
    # print(f"✓ 读取了 {len(x)} 个点")
    
    # 示例：保存输出文件
    # output_file = get_output_path("output_result.tif")
    # 保存处理结果到 output_file
    
    print("✓ 处理完成")

if __name__ == "__main__":
    main()
