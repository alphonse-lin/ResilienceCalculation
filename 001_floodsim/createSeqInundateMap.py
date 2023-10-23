import os
import re
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utilis.general import timeCount, mkdir, getfiles

import rasterio
import geopandas as gpd
from shapely.geometry import box
import numpy as np
import pandas as pd
import warnings

# 提取文件名中的数字，如果没有数字则返回0
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0



if __name__ == '__main__':
    # 第二步：生成连续淹没地图
    # 禁用所有警告
    warnings.filterwarnings('ignore')
    # 将科学计数法输出关闭
    np.set_printoptions(suppress=True)

    input_dir=r'D:\Code\114_temp\008_CodeCollection\001_python\009_ResilienceCalculation\data\output\output\output'
    road_data_path=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\network_transfer.geojson'
    output_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\002_event'
    
    # 加载GeoJSON文件
    road_network = gpd.read_file(road_data_path)
    files=getfiles(input_dir)
    # 对文件列表进行排序
    sorted_files = sorted(files, key=extract_number)
    
    flag_dic={}
    depth_dic={}
    ids=[]
    for file in sorted_files:
        if 'h_' in file and '.asc' in file and 'max' not in file:
            flood_map_path=os.path.join(input_dir,file)
            temp_attr=file.split('.')[0]

            # 加载ASC文件
            with rasterio.open(flood_map_path) as asc:
                flood_map = asc.read(1)  # 读取数据

            ## 创建一个用于存储被淹没的路段的GeoDataFrame
            # flooded_roads = gpd.GeoDataFrame(columns=road_network.columns, crs=road_network.crs)

            # 遍历每个路段，检查是否有洪水
            depths=[]
            flags=[]
            for i, row in road_network.iterrows():
                road_geometry = row.geometry

                # 获取这个路段的边界，并转化为raster坐标系
                road_bounds = road_geometry.bounds
                minx, miny, maxx, maxy = road_bounds
                left, bottom = rasterio.transform.rowcol(asc.transform, minx, miny)
                right, top = rasterio.transform.rowcol(asc.transform, maxx, maxy)

                # 检查这个边界内是否有洪水，洪水定义为洪水地图数值超过3
                # print(flood_map[min(left, right):max(left, right), min(top, bottom):max(top, bottom)])
                if temp_attr=='h_0':
                    ids.append(int(row['id']))

                check_value=flood_map[min(left, right):max(left, right), min(top, bottom):max(top, bottom)]
                if check_value.size > 0:
                    max_value = np.max(check_value)
                else:
                    max_value = 0

                depths.append(max_value)

                if (check_value > 3).any():
                    # 如果有洪水，将这个路段添加到flooded_roads
                    flags.append(1)
                else:
                    flags.append(0)
            flag_dic[temp_attr]=flags
            depth_dic[f'{temp_attr}_depth']=depths
            print(f'finished {temp_attr}')
        flag_dic['id']=ids
        depth_dic['id']=ids
    
    flag_df = pd.DataFrame(flag_dic)
    flag_df.sort_values(by=['id'], inplace=True, ascending=True)
    flag_df.to_csv(os.path.join(output_dir,'flag_sequenced_flooded_roads_1.csv'), index=False)

    depth_df = pd.DataFrame(depth_dic)
    depth_df.sort_values(by=['id'], inplace=True, ascending=True)
    depth_df.to_csv(os.path.join(output_dir,'depth_sequenced_flooded_roads_1.csv'), index=False)
