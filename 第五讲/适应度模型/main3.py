#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/5/22 16:37

"""
导言：本期目标是对BA无标度网络的度动力学进行建模，重点介绍了节点的度k(t)随时间t的演变关系。
"""
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


# print(matplotlib.get_backend())

def barabasi_albert_graph(n0, n, m, i0, i1, i2):
    # 假定初始网络是一个包含n0个节点的完全网络
    G = nx.complete_graph(n0)
    targets = list(range(m))
    repeated_nodes = list(range(n0))*m
    source = n0
    deg_i0 = []
    deg_i1 = []
    deg_i2 = []
    while source < n:
        degree_list = [G.degree(i) for i in G.nodes()]
        if i0 < len(G.nodes()):
            deg_i0.append(degree_list[i0])
        if i1 < len(G.nodes()):
            deg_i1.append(degree_list[i1])
        if i2 < len(G.nodes()):
            deg_i2.append(degree_list[i2])
        G.add_edges_from(zip([source] * m, targets))
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source] * m)
        targets = random.sample(repeated_nodes, m)
        targets = set(targets)
        while len(targets) < m:
            x = random.choice(repeated_nodes)
            targets.add(x)
        source += 1
    return G, deg_i0, deg_i1, deg_i2


if __name__ == '__main__':
    n0 = 3
    m = 2
    n = 10000
    etas = np.random.uniform(0, 1, n)

    # 设置指定节点的适应度值
    i0, i1, i2 = 1, 10, 100

    samples = 10
    y0 = np.zeros(9997)
    y1 = np.zeros(9989)
    y2 = np.zeros(9899)
    for i in range(samples):
        G, deg_i0, deg_i1, deg_i2 = barabasi_albert_graph(n0, n, m, i0, i1, i2)
        y0 += np.array(deg_i0)
        y1 += np.array(deg_i1)
        y2 += np.array(deg_i2)

    # print(len(deg_i0),len(deg_i1),len(deg_i2))

    x = list(range(1,n+1))
    xx0 = np.arange(x[0], x[len(x) - 1], 0.01)
    yy0 = (10 ** 1) * xx0 ** (0.5)
    print("==============")


    # 绘制指定节点的度与时间的依赖关系
    # plt.plot(range(i0, i0+len(deg_i0)), deg_i0, 'r-', label='node '+str(i0))
    # plt.plot(range(i1, i1+len(deg_i1)), deg_i1, 'b-', label='node '+str(i1))
    # plt.plot(range(i2, i2+len(deg_i2)), deg_i2, 'g-', label='node '+str(i2))
    plt.plot(range(i0, i0+len(y0)), y0/samples, 'r-', label='node '+str(i0))
    plt.plot(range(i1, i1+len(y1)), y1/samples, 'b-', label='node '+str(i1))
    plt.plot(range(i2, i2+len(y2)), y2/samples, 'g-', label='node '+str(i2))
    plt.plot(xx0, yy0, "k--", linewidth=1.0, label=r'$k(t) \sim t^{\beta}, \beta = 0.5$')

    plt.legend(loc=0)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel('$t$')
    plt.ylabel('$k(t)$')
    plt.savefig("BA.pdf")
    # plt.show()
