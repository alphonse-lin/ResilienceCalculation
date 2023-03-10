import networkx as nx
from geopandas import read_file, sjoin, GeoDataFrame
import matplotlib.pyplot as plt
import time
import numpy
import os

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
    roadPath = r'data\part_london\TQ27ne_RoadNetwork_single.geojson'
    output_dir= r'data\output\geojson'
    # blockPath = r'D:\UrbanXLab\Urban_Design_Tool\Blocks-Indicators\blocks\{0}.shp'.format(city)
    # outputBlockPath = r'D:\UrbanXLab\Urban_Design_Tool\Blocks-Indicators\blocks_info\{0}_blocks_betweenness.csv'.format(city)

    df = read_file(roadPath)
    G = gdf2graph(df)
    H = nodegraph2edgegraph(G)
    timeCount("construct graph",t_start)
    # nx.draw(G, pos=nx.spectral_layout(G))
    # plt.show()

    la_max=nx.laplacian_matrix(G).toarray()
    numpy.savetxt(os.path.join(output_dir,"laplacian_max"), la_max, delimiter=',')
    timeCount("construct laplacian_max",t_start)

    nx.write_adjlist(H, os.path.join(output_dir,"edgeGraph.adjlist"))
    timeCount("save adjlist",t_start)

    bet_nodes = nx.betweenness_centrality(H, normalized=True, weight="weight")
    timeCount("betweeness",t_start)

    clo_nodes = nx.closeness_centrality(H)
    timeCount("closeness",t_start)

    df["betweenness"] = 0
    df["closeness"] = 0

    for i in range(len(df)):
        if bet_nodes.get(i) is not None:
            df.loc[i, "betweenness"] = bet_nodes[i]
        else:
            df.loc[i, "betweenness"] = -1
        if clo_nodes.get(i) is not None:
            df.loc[i, "closeness"] = clo_nodes[i]
        else:
            df.loc[i, "closeness"] = -1
    df.to_file(os.path.join(output_dir, "roadnetwork_bet.geojson"), driver='GeoJSON')
    timeCount("export", t_start)

    ### Process the blocks
    # blocks = read_file(blockPath)
    # blocks_buffer = blocks.buffer(distance=buffer_dist)
    # blocks = GeoDataFrame(blocks["id"], geometry=blocks_buffer)
    # df = df.loc[df["betweenness"] != -1,].reset_index().drop(["index"], axis=1)
    # temp = sjoin(blocks, df, how='left', op='intersects')
    # final = temp.groupby(['id'], as_index=False)[["betweenness"]].mean()
    # final.to_csv(outputBlockPath, index=False)

    # temp3 = merge(blocks, final, how='left', on='id')
    # temp3.to_file(r'D:\UrbanXLab\Urban_Design_Tool\Blocks-Indicators\blocks_info\temp2.geojson', driver='GeoJSON')