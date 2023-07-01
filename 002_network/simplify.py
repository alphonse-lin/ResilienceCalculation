import geopandas as gpd
from shapely.geometry import MultiLineString, MultiPolygon, LineString, Polygon
from shapely.ops import unary_union

if __name__ == '__main__':

    input_path= r'data\part_london\tq38sw_2m\roadnetwork_1.geojson'
    output_path= r'data\output\geojson\roadnetwork_1_simplify.geojson'
    # 定义需要转换的几何类型
    MULTI_TYPES = [MultiLineString, MultiPolygon]

    # 读取包含多几何对象的 shapefile 文件
    gdf = gpd.read_file(input_path)

    # 创建一个空的 GeoDataFrame
    new_gdf = gpd.GeoDataFrame()

    # 处理每个几何对象
    for index, row in gdf.iterrows():
        # 获取几何对象和类型
        geom = row['geometry']
        geom_type = type(geom)
        
        # 如果几何对象是需要转换的类型之一
        if geom_type in MULTI_TYPES:
            # print(f"Original {geom_type.__name__}:", geom)
            
            # 将多几何对象转换为单一几何对象
            single_geom = unary_union(geom)
            single_type = type(single_geom)
            
            # 如果转换后的几何对象是需要的类型之一
            if not single_type in MULTI_TYPES:
                # print(f"Converted {geom_type.__name__} to {single_type.__name__}:", single_geom)
                
                # 获取几何对象的属性数据
                attrs = row.drop(labels=['geometry'])
                
                # 将单一几何对象和属性数据添加到新的 GeoDataFrame 中
                new_row = attrs.to_dict()
                new_row['geometry'] = single_geom
                new_gdf = new_gdf.append(new_row, ignore_index=True)
        # else:
        #         # 如果几何对象不是需要转换的类型之一
        #         print(f"Skipping {geom_type.__name__}:", geom)

        # 将结果保存到 GeoJSON 文件中
    new_gdf_2 = gpd.GeoDataFrame(new_gdf, geometry='geometry')
    new_gdf_2.to_file(output_path, driver='GeoJSON')
