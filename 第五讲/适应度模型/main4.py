#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/5/22 16:37

"""
导言：本期目标是对比安科尼－巴拉巴西网络的度动力学进行建模，重点介绍了不同适应度节点的度k(t)随时间t的演变关系。
"""
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

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

# 适应度模型
def bianconi_barabasi_model(n0, m, n, etas, i0, i1, i2):
    """create Bianconi-Barabási（比安科尼－巴拉巴西模型）Model"""
    # 假设初始网络是一个完全网络
    G = nx.complete_graph(n0)
    deg_i0 = []
    deg_i1 = []
    deg_i2 = []
    # 增加新节点
    for i in range(n0, n):
        counter = 0
        available = list(G.nodes())
        degree_list = [G.degree(i) for i in available]
        if i0 < len(G.nodes()):
            deg_i0.append(degree_list[i0])
        if i1 < len(G.nodes()):
            deg_i1.append(degree_list[i1])
        if i2 < len(G.nodes()):
            deg_i2.append(degree_list[i2])

        while counter < m:
            degree_dst = [G.degree(node) for node in available]
            fitness = np.multiply(degree_dst, [etas[node] for node in available])
            fitness_prob = dict(zip(available, fitness/fitness.sum()))
            selected = np.random.choice(available, p=list(fitness_prob.values()))

            # 在available移除selected
            available.remove(selected)
            del fitness_prob[selected]

            # 增加连边
            G.add_edge(i, selected)
            counter += 1

    return G, deg_i0, deg_i1, deg_i2



if __name__ == '__main__':
    n0 = 3
    m = 2
    n = 10000
    etas = np.random.uniform(0, 1, n)

    # 设置指定节点的适应度值
    i0, i1, i2 = 1, 10, 100
    etas[i0] = 0.2
    etas[i1] = 0.5
    etas[i2] = 0.99


    samples = 10
    y0 = np.zeros(9997)
    y1 = np.zeros(9989)
    y2 = np.zeros(9899)
    for i in range(samples):
        G, deg_i0, deg_i1, deg_i2 = bianconi_barabasi_model(n0, m, n, etas, i0, i1, i2)
        y0 += np.array(deg_i0)
        y1 += np.array(deg_i1)
        y2 += np.array(deg_i2)

    # 绘制指定节点的度与时间的依赖关系
    plt.plot(range(i0, i0 + len(y0)), y0 / samples, 'r-', label=r'$\eta = $'+str(etas[i0]))
    plt.plot(range(i1, i1 + len(y1)), y1 / samples, 'b-', label=r'$\eta = $' + str(etas[i1]))
    plt.plot(range(i2, i2 + len(y2)), y2 / samples, 'g-', label=r'$\eta = $' + str(etas[i2]))


    # plt.plot(range(i0, i0+len(deg_i0)), deg_i0, 'ro', label=r'$\eta = $'+str(etas[i0]))
    # plt.plot(range(i1, i1 + len(deg_i1)), deg_i1, 'bo', label=r'$\eta = $' + str(etas[i1]))
    # plt.plot(range(i2, i2 + len(deg_i2)), deg_i2, 'go', label=r'$\eta = $' + str(etas[i2]))


    # a = np.array(range(i0, i0 + len(deg_i0)))
    # step = 100
    # b = list(range(1, n, step))
    # x0 = a[b]
    # y0 = np.array(deg_i0)[b]
    #
    # a = np.array(range(i1, i1 + len(deg_i1)))
    # step = 100
    # b = list(range(1, n - i1, step))
    # x1 = a[b]
    # y1 = np.array(deg_i1)[b]
    #
    # a = np.array(range(i2, i2 + len(deg_i2)))
    # step = 100
    # b = list(range(1, n - i2, step))
    # x2 = a[b]
    # y2 = np.array(deg_i2)[b]
    #
    # plt.plot(x0, y0, 'ro-', label=r'$\eta = $'+str(etas[i0]))
    # plt.plot(x1, y1, 'bo-', label=r'$\eta = $'+str(etas[i1]))
    # plt.plot(x2, y2, 'go-', label=r'$\eta = $'+str(etas[i2]))

    plt.legend(loc=0)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel('$t$')
    plt.ylabel('$k(t)$')
    plt.savefig("BB.pdf")
    # plt.show()
