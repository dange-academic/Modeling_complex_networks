#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/5/14 16:56


import random
import networkx as nx
import matplotlib.pyplot as plt
plt.rc('font', family='SimHei')



def barabasi_albert_graph(n0, n, m):
    # 假定初始网络是一个包含n0个节点的完全网络
    G = nx.complete_graph(n0)
    targets = list(range(m))

    repeated_nodes = list(range(n0))*m

    source = n0
    while source < n:
        G.add_edges_from(zip([source] * m, targets))
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source] * m)
        targets = random.sample(repeated_nodes, m)
        targets = set(targets)
        while len(targets) < m:
            x = random.choice(repeated_nodes)
            targets.add(x)
        source += 1
    return G


n0 = 3
m = 3

N = [10,20,30,50,70,100,200,300,400,500,700,1000,2000]

# 计算BA无标度网络的平均距离、平均集聚系数与尺寸N的依赖关系
C = [] # 平均集聚系数
L = [] # 平均距离
samples = 1
for n in N:
    s1 = 0
    s2 = 0
    for i in range(samples):
        G = barabasi_albert_graph(n0, n, m)
        s1 += nx.average_clustering(G)
        s2 += nx.average_shortest_path_length(G)

    C.append(s1 / samples)
    L.append(s2 / samples)

print("=============")


plt.figure(figsize=(10,4))
plt.subplot(121)
plt.plot(N, C, 'ro')
plt.xlabel("$N$")
plt.ylabel("$<C>$")
plt.xscale("log")
# plt.yscale("log")
plt.title("平均集聚系数")

plt.subplot(122)
plt.plot(N, L, 'bs')
plt.xlabel("$N$")
plt.ylabel("$<d>$")
plt.xscale("log")
plt.title("平均距离")


plt.savefig("BA_C_L.png", dpi=600)
plt.show()