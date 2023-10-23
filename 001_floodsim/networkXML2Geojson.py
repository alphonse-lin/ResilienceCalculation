from lxml import etree
import geopandas as gpd
from shapely.geometry import LineString
import os

if __name__ == "__main__":
    # 第一步：Matsim网络转换为GeoJSON
    input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry\output_4-00-pm\output_network.xml'
    # 解析XML数据
    xml_path=os.path.join(input_dir, 'output_network.xml')
    root = etree.parse(xml_path).getroot()

    # 从XML中提取nodes，并存入字典
    nodes = {node.attrib['id']: (float(node.attrib['x']), float(node.attrib['y']))
            for node in root.xpath('//nodes/node')}

    # 从XML中提取links，并转换成LineString格式
    links = [{'id': int(link.attrib['id']),
            'geometry': LineString([nodes[link.attrib['from']], nodes[link.attrib['to']]]),
            'freespeed': float(link.attrib['freespeed']),
            'capacity': float(link.attrib['capacity']),
            'permlanes': float(link.attrib['permlanes']),
            'oneway': int(link.attrib['oneway']),
            'modes': link.attrib['modes']}
            for link in root.xpath('//links/link')]

    # 转换为GeoDataFrame
    gdf = gpd.GeoDataFrame(links, crs="EPSG:27700")  # 这里使用WGS84坐标系，你可以根据需要替换为其他坐标系
    gdf.sort_values(by='id', inplace=True)  # 按照id排序

    # 输出为GeoJSON
    gdf.to_file(os.path.join(input_dir, "network_transfer.geojson"), driver='GeoJSON')
    print("finished")
