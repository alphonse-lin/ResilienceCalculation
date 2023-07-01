import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString,MultiLineString
from shapely.ops import linemerge
import os

if __name__ == '__main__':
    output_dir=r'data\hereMap\geojson'
    input_dir=r'data\hereMap\mapdata_saved'
    file_list=os.listdir(input_dir)
    for file in file_list:
        file_path=os.path.join(input_dir,file)
        file_name=file.split('.')[0]

        # 从文件中读取JSON数据
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # 访问JSON数据中的元素
        res_gdf=gpd.GeoDataFrame()
        lines=[]
        speed=[]
        speedUncapped=[]
        freeFlow=[]
        jamFactor=[]
        confidence=[]
        traversability=[]
        for i in range(len(data["results"])):   
            item=data["results"][i]
            temp_links=item["location"]['shape']['links']
            temp_flow=item["currentFlow"]
            temp_ls=[]
            coords_list=[]
            for j in range(len(temp_links)):
                for k in range(len(temp_links[j]['points'])):
                    coords = [Point(feature['lng'], feature['lat']) for feature in temp_links[j]['points']]
                    coords_list.extend(coords)
            # 定义空字典
            pts_dict = {}

            # 遍历列表，将元组作为键，将值设置为True
            for item in coords_list:
                pts_dict[item] = True
                    # points = gpd.GeoSeries([Point(x, y) for x, y in coords])
                    # line = LineString(points)
                    # temp_ls.append(line)
            # 获取字典的键，即为去重后的元组列表
            new_pts = list(pts_dict.keys())

            # 将点转换为线段
            line = LineString([(p.x, p.y) for p in new_pts])
            lines.append(line)

        #     points = gpd.GeoSeries(my_unique_list)
        #     line = LineString(points)
        #     print(line)
        #     lines.append(line)
            speed.append(temp_flow.get('speed',0))
            speedUncapped.append(temp_flow.get('speedUncapped',0))
            freeFlow.append(temp_flow.get('freeFlow',0))
            jamFactor.append(temp_flow.get('jamFactor',0))
            confidence.append(temp_flow.get('confidence',0))
            traversability.append(temp_flow.get('traversability',0))

        buffer_df = pd.DataFrame({'speed': speed, 'speedUncapped': speedUncapped, 'freeFlow': freeFlow, 'jamFactor': jamFactor, 'confidence': confidence, 'traversability': traversability})
        buffer_gdf = gpd.GeoDataFrame(buffer_df, geometry=lines)
        
        output_file_path=os.path.join(output_dir, f'{file_name}.geojson')
        buffer_gdf.to_file(output_file_path,driver='GeoJSON')
        print(f"exported----------{output_file_path}")