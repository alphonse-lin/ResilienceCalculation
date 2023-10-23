import rasterio
import geopandas as gpd
from shapely.geometry import box
import os
import numpy as np
import pandas as pd
import warnings

# 禁用所有警告
warnings.filterwarnings('ignore')

# 将科学计数法输出关闭
np.set_printoptions(suppress=True)

time_step=5400
flood_map_path=r'D:\Code\114_temp\008_CodeCollection\001_python\009_ResilienceCalculation\data\output\output\output\h_{0}.asc'.format(time_step)
road_data_path=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\output_ucl\001\r_-1\1000\network_transfer.geojson'

output_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london'

# 加载ASC文件
with rasterio.open(flood_map_path) as asc:
    flood_map = asc.read(1)  # 读取数据

# 加载GeoJSON文件
road_network = gpd.read_file(road_data_path)

# 创建一个用于存储被淹没的路段的GeoDataFrame
flooded_roads = gpd.GeoDataFrame(columns=road_network.columns, crs=road_network.crs)

# 遍历每个路段，检查是否有洪水
ids=[]
depth=[]
for i, row in road_network.iterrows():
    road_geometry = row.geometry

    # 获取这个路段的边界，并转化为raster坐标系
    road_bounds = road_geometry.bounds
    minx, miny, maxx, maxy = road_bounds
    left, bottom = rasterio.transform.rowcol(asc.transform, minx, miny)
    right, top = rasterio.transform.rowcol(asc.transform, maxx, maxy)

    # 检查这个边界内是否有洪水，洪水定义为洪水地图数值超过3
    # print(flood_map[min(left, right):max(left, right), min(top, bottom):max(top, bottom)])
    check_value=flood_map[min(left, right):max(left, right), min(top, bottom):max(top, bottom)]
    if (check_value > 2).any():
        # 如果有洪水，将这个路段添加到flooded_roads
        flooded_roads = flooded_roads.append(row)
        max_value=np.max(check_value)
        depth.append(max_value)
        ids.append(row['id'])

# 将flooded_roads输出到一个新的文件
output_csv=os.path.join(output_dir,f'flooded_roads_{time_step}.csv')
df = pd.DataFrame({'id': ids, 'depth': depth})

# 将DataFrame对象输出为csv文件

df.to_csv(output_csv, index=False)

# output_geojson=os.path.join(output_dir,f'flooded_roads_{time_step}.geojson')
# flooded_roads['id']=ids
# flooded_roads['depth']=depth
# flooded_roads.to_file(output_geojson, driver='GeoJSON')
print(output_csv)
print("finished")
