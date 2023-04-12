# -*- encoding: utf-8 -*-
'''
@File  :   intentional_attack.py
@Date  :   2023/04/12 21:27:29
@Author:   单哥
@Email :   chend_zqfpu@163.com
'''
# 蓄意攻击：
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
plt.rc('font', family='SimHei')

# 创建一个1000个节点的无标度网络
n, m = 1000, 3
G = nx.barabasi_albert_graph(n, m)

# 计算原始网络的巨连通分支大小
largest_cc = max(nx.connected_components(G), key=len)
initial_size = len(largest_cc) / n


# 静态攻击：始终在初始网络上攻击，按照节点度值大小将占比为f的节点移除，并计算剩余网络的巨连通分支相对大小
# 获取初始网络节点度值排序后的列表
degrees = dict(G.degree())
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

nums = 51
f_values = np.linspace(0, 1, num=nums)
relative_sizes = np.zeros(nums)
relative_sizes[0] = initial_size
for i in range(1, nums):
    # 计算要移除的节点列表
    num_removed = int(f_values[i] * n)
    removed_nodes = [x[0] for x in sorted_degrees[:num_removed]]

    # 移除节点并计算剩余网络的巨连通分支大小
    G_removed = G.copy()
    G_removed.remove_nodes_from(removed_nodes)
    if len(G_removed)==0:
        break
    largest_cc_removed = max(nx.connected_components(G_removed), key=len)
    relative_sizes[i] = len(largest_cc_removed) / n



# # 动态攻击：在当前始网络上攻击，每攻击一次要重新计算度值排序
# n_end = n
# step = 20
# if n_end % step == 0:
#     nums = int(n_end / step)
# else:
#     nums = int(n_end / step) + 1
#
# f_values = np.linspace(0, n_end, nums) / n
# relative_sizes = np.zeros(nums)
# relative_sizes[0] = initial_size
# G_removed = G.copy()
# for i in range(1, nums):
#     # 获取节点度值排序后的列表
#     degrees = dict(G_removed.degree())
#     sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
#
#     # 计算要移除的节点列表
#     removed_nodes = [x[0] for x in sorted_degrees[:step]]
#
#     # 移除节点并计算剩余网络的巨连通分支大小
#     G_removed.remove_nodes_from(removed_nodes)
#     if len(G_removed)==0:
#         break
#     largest_cc_removed = max(nx.connected_components(G_removed), key=len)
#     relative_sizes[i] = len(largest_cc_removed) / n


# 绘制相对大小随着占比f的变化图
plt.plot(f_values, relative_sizes, 'ro-', linewidth=2)
plt.xlabel('占比 f')
plt.ylabel('巨连通分支相对大小')
plt.title('蓄意攻击')
plt.show()
