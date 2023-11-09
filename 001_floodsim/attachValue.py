import geopandas as gpd
import os

# Extra: Add an id column to the GeoJSON file
if __name__ == '__main__':
    road_data_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london'
    road_data_path=os.path.join(road_data_dir,'roadnetwork_1.geojson')
    # 读取geojson文件
    gdf = gpd.read_file(road_data_path)

    # 添加自增的id数值
    gdf['id'] = range(0, len(gdf))

    # 将flooded_roads输出到一个新的GeoJSON文件
    output_path=os.path.join(road_data_dir,'roadnetwork_id.geojson')
    gdf.to_file(output_path, driver='GeoJSON')