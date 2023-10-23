import networkx as nx
import matplotlib.pyplot as plt

# 创建一个有向图
G = nx.DiGraph()
G.add_edges_from([
    (1, 2), (2, 3), (3, 4), (4, 2),  # SCC 1
    (5, 6), (6, 7), (7, 5),  # SCC 2
    (8, 9),  # SCC 3
    (3, 5), (8, 4)  # 连接不同SCC的边
])

# 找到强连通分量
scc = list(nx.strongly_connected_components(G))

# 输出强连通分量
print("Strongly Connected Components:")
for i, component in enumerate(scc):
    print(f"Component {i + 1}: {component}")

# 可视化图
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
plt.title("Directed Graph")
plt.show()
