# import numpy as np
# from scipy.sparse.linalg import eigsh

# # 定义谱中心性计算函数
# def spectral_centrality(W, k):
#     # 构建拉普拉斯矩阵
#     D = np.diag(np.sum(W, axis=0))
#     L = D - W
#     # 计算特征值和特征向量
#     eig_vals, eig_vecs = eigsh(L, k=k, which='SM')
#     # 对特征向量进行归一化
#     Y = eig_vecs / np.linalg.norm(eig_vecs, axis=0)
#     # 计算谱中心性
#     centrality = np.sum(Y**2, axis=1)
#     return centrality

# # 测试
# W = np.array([[0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0]])
# W=W.astype(np.float)
# centrality = spectral_centrality(W, 2)
# print(centrality)


import networkx as nx
from geopandas import read_file, sjoin, GeoDataFrame
import matplotlib.pyplot as plt
import time
import numpy as np
import os
from shapely.ops import unary_union

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utilis.general import timeCount, mkdir


def round_tuple(x, digits):
    new_tuple = tuple(round(a, digits) for a in x)
    return new_tuple


def gdf2graph(df):
    o_list = []
    d_list = []
    len_list = []

    for i in range(len(df)):
        this_line = df.loc[i, "geometry"]
        this_len = this_line.length

        first_point = this_line.coords[0]
        last_point = this_line.coords[-1]

        first_point = round_tuple(first_point, 3)
        last_point = round_tuple(last_point, 3)

        o_list.append(first_point)
        d_list.append(last_point)
        len_list.append(this_len)

    edge_list = [(x, y) for x, y in zip(o_list, d_list)]
    G = nx.Graph(edge_list)
    for i in range(len(len_list)):
        G.edges[o_list[i], d_list[i]]["weight"] = len_list[i]
        G.edges[o_list[i], d_list[i]]["id"] = i
    return G


def nodegraph2edgegraph(G):
    H = nx.Graph()
    for node in G.nodes:
        neighbours = list(G.neighbors(node))
        neigh_edges = [(node, x) for x in neighbours]
        neigh_attrs = [G.get_edge_data(x[0], x[1]) for x in neigh_edges]
        for i in range(len(neigh_edges) - 1):
            for j in range(i + 1, len(neigh_edges)):
                # new_weight = (neigh_attrs[i]["weight"] + neigh_attrs[j]["weight"]) / 2
                new_weight = 1
                H.add_edge(neigh_attrs[i]["id"], neigh_attrs[j]["id"], weight=new_weight, mynode=node)
    return H


if __name__ == '__main__':
    t_start=time.time()
    roadPath = r'data\output\geojson\roadnetwork_1_simplify.geojson'
    output_dir= r'data\output\geojson'
    # blockPath = r'D:\UrbanXLab\Urban_Design_Tool\Blocks-Indicators\blocks\{0}.shp'.format(city)
    # outputBlockPath = r'D:\UrbanXLab\Urban_Design_Tool\Blocks-Indicators\blocks_info\{0}_blocks_betweenness.csv'.format(city)

    gdf = read_file(roadPath)
    # 将多部分几何图形拆分为单一几何对象
    G = gdf2graph(gdf)
    H = nodegraph2edgegraph(G)
    timeCount("construct graph",t_start)
    # nx.draw(G, pos=nx.spectral_layout(G))
    # plt.show()

    # 计算拉普拉斯矩阵的特征值和特征向量
    laplacian_matrix = nx.laplacian_matrix(H).todense()
    eigenvalues, eigenvectors = np.linalg.eig(laplacian_matrix)
    timeCount("计算拉普拉斯矩阵的特征值和特征向量",t_start)

    # 找到最小的非零特征值的索引
    min_nonzero_index = np.argmin(np.abs(eigenvalues[1:]))
    timeCount("找到最小的非零特征值的索引",t_start)

    # 找到对应的特征向量
    second_smallest_eigenvector = eigenvectors[:, min_nonzero_index + 1]
    timeCount("找到对应的特征向量",t_start)

    # 计算谱中心性
    spectral_centrality = nx.eigenvector_centrality_numpy(H, weight='weight')
    timeCount("计算谱中心性",t_start)
    
    keys_array = np.array(list(spectral_centrality.keys()))
    values_array = np.array(list(spectral_centrality.values()))
    combined_array = np.column_stack((keys_array, values_array))
    # 设置打印选项
    np.set_printoptions(suppress=True)
    np.savetxt(os.path.join(output_dir, 'spectral_centrality.csv'), combined_array, delimiter=',', fmt='%s')
    # # # 打印结果
    print("谱中心性:", spectral_centrality)
    # # timeCount("打印结果",t_start)

    # # 将谱中心性的值赋值到 GeoJSON 文件中
    # tmp_value=list(spectral_centrality.values())
    # for i, row in gdf.iterrows():
    #     gdf.at[i, 'spectral_centrality'] = tmp_value[i]

    # # 将修改后的 GeoJSON 文件写入磁盘
    # gdf.to_file('output_spectral_centrality.geojson', driver='GeoJSON')