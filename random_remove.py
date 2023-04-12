# -*- encoding: utf-8 -*-
'''
@File  :   random_remove.py
@Date  :   2023/04/12 21:25:56
@Author:   单哥
@Email :   chend_zqfpu@163.com
'''
# 随机攻击：随机攻击一般需要设置多个样本求平均值，以下是单个样本
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
plt.rc('font', family='SimHei')

# 创建一个1000个节点的无标度网络
n, m = 1000, 3
G = nx.barabasi_albert_graph(n, m)

# 计算原始网络的巨连通分支大小
largest_cc = max(nx.connected_components(G), key=len)
initial_size = len(largest_cc) / len(G)

# 计算不同占比f下剩余网络的巨连通分支相对大小
f_values = np.linspace(0, 1, num=101)
relative_sizes = np.zeros(101)
for i, f in enumerate(f_values):
    # 随机移除占比为f的节点
    removed_nodes = np.random.choice(G.nodes(), size=int(f * len(G)), replace=False)
    G_removed = G.copy()
    G_removed.remove_nodes_from(removed_nodes)
    if len(G_removed)==0:
        break


    # 计算剩余网络的巨连通分支大小
    largest_cc_removed = max(nx.connected_components(G_removed), key=len)
    relative_sizes[i] = len(largest_cc_removed) / len(G)

# 绘制相对大小随着占比f的变化图
plt.plot(f_values, relative_sizes, 'ro-')
plt.xlabel('占比 f')
plt.ylabel('巨连通分支相对大小')
plt.title('随机攻击')
plt.show()
