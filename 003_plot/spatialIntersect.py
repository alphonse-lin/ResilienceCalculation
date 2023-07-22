import geopandas as gpd
import os
import seaborn as sns
import matplotlib.pyplot as plt

file_dir=r'data\hereMap\geojson'
boundary_file=r'data\hereMap\matsim_count\output_events_12.geojson'
output_dir=r'data\hereMap\intersect'

temp_gdf2 = gpd.read_file(boundary_file)
temp_gdf2.crs = {'init': 'epsg:27700'}
gdf2 = temp_gdf2.to_crs(epsg=4326)
# gdf2.to_file(r'data\hereMap\matsim_count\output_12_4326.geojson', driver='GeoJSON')

for filename in os.listdir(file_dir):
    temp_path=os.path.join(file_dir,filename)

    gdf1 = gpd.read_file(temp_path)
    # 空间相交
    intersect = gpd.sjoin(gdf1, gdf2, how="inner", predicate='intersects')
    gdf_27700 = intersect.to_crs(epsg=27700)

    # # 计算相关系数矩阵
    # corr = intersect.head(400).corr()
    # # 绘制热力图
    # sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    # plt.show()

    # 将相交结果输出为geojson文件
    output_path=os.path.join(output_dir,f'intersect_{filename}.geojson')
    
    gdf_27700.to_file(output_path, driver='GeoJSON')
    print(filename)


