import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# 创建一个简单的图
G = nx.Graph()
edges = [(1,2), (2,3), (3,4), (4,1), (1,5)]
G.add_edges_from(edges)

# # 画出图的结构
# nx.draw(G, with_labels=True)
# plt.show()

# 计算拉普拉斯矩阵
L = nx.laplacian_matrix(G).toarray()

# 初始条件: 我们让节点1的初始值为1，其他节点为0
phi_0 = np.zeros(len(G.nodes()))
phi_0[0] = 1

# 扩散参数
alpha = 0.1

# 时间步长和时间点数量
dt = 0.1
time_steps = 100

# 记录扩散过程
phi_t = np.zeros((time_steps, len(G.nodes())))
phi_t[0] = phi_0

# 迭代计算
for t in range(1, time_steps):
    phi_t[t] = phi_t[t-1] - alpha * np.dot(L, phi_t[t-1]) * dt

# 选择一个节点进行绘图
node_idx = 0

# 画出这个节点上的扩散过程
plt.plot(np.arange(time_steps) * dt, phi_t[:, node_idx])
plt.xlabel('Time')
plt.ylabel(f'Value at Node {node_idx + 1}')
plt.title(f'Diffusion Process at Node {node_idx + 1}')
plt.show()

