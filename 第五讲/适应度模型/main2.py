#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/5/22 16:37

import networkx as nx
import numpy as np
import powerlaw
import matplotlib.pyplot as plt
import igraph as ig
import random

def barabasi_albert_graph(n0, n, m):
    # 假定初始网络是一个包含n0个节点的完全网络
    G = nx.complete_graph(n0)
    targets = list(range(m))

    repeated_nodes = list(range(n0))*m

    degree_hist = []
    source = n0
    while source < n:
        degree_hist.append([G.degree(node) for node in G.nodes()])
        G.add_edges_from(zip([source] * m, targets))
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source] * m)
        targets = random.sample(repeated_nodes, m)
        targets = set(targets)
        while len(targets) < m:
            x = random.choice(repeated_nodes)
            targets.add(x)
        source += 1
    return G, degree_hist


def create_bb_model(n0, m, n, etas):
    """create Bianconi-Barabási（比安科尼－巴拉巴西模型）Model"""
    # 假设初始网络是一个完全网络
    BB = nx.complete_graph(n0)
    degree_hist = []
    # 增加新节点
    for i in range(n0, n):
        counter = 0
        available = list(BB.nodes())
        degree_hist.append([BB.degree(node) for node in available])
        while counter < m:
            degree_dst = [BB.degree(node) for node in available]
            fitness = np.multiply(degree_dst, [etas[node] for node in available])
            fitness_prob = dict(zip(available, fitness/fitness.sum()))
            selected = np.random.choice(available, p=list(fitness_prob.values()))

            # 在available移除selected
            available.remove(selected)
            del fitness_prob[selected]

            # 增加连边
            BB.add_edge(i, selected)
            counter += 1

    return BB, degree_hist


if __name__ == '__main__':
    n0 = 3
    m = 2
    n = 5000
    etas = np.random.uniform(0, 1, n)

    # 设置指定节点的适应度值
    i0, i1, i2 = 4, 14, 104
    # etas[1000] = 0.2
    # etas[3000] = 0.35
    # etas[5000] = 0.85
    # G, degree_hist = create_bb_model(n0, m, n, etas)

    G, degree_hist = barabasi_albert_graph(n0, n, m)
    print(len(degree_hist))
    print(len(range(i0 + 1, n)), len(degree_hist[(i0 - n0 + 1):]))




    # 绘制指定节点的度与时间的依赖关系
    plt.plot(range(i0 + 1, n), [i[i0] for i in degree_hist[(i0 - n0 + 1):]], 'r-', label=r'node 1, $\eta = 0.2$')
    plt.plot(range(i1 + 1, n), [i[i1] for i in degree_hist[(i1 - n0 + 1):]], 'b-', label=r'node 100, $\eta = 0.36$')
    plt.plot(range(i2 + 1, n), [i[i2] for i in degree_hist[(i2 - n0 + 1):]], 'g-', label=r'node 500, $\eta = 0.85$')

    plt.legend(loc=0)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel('$t$')
    plt.ylabel('$k(t)$')
    plt.show()







    # G = ig.Graph.Static_Fitness(n, etas, fitness_in=None, loops=False, multiple=False)
    # # ig.plot(G)
    # degree_seq = G.degree()
    # degree_seq = [i for i in degree_seq if i != 0]
    # print(degree_seq)





    # print("===========")
    # # 对数坐标，对数分箱
    # powerlaw.plot_pdf(degree_seq, linear_bins=False, color='r', marker='o', linewidth=0.0, label='$N = 1000$')
    # plt.legend(loc=0)
    # print("===========")
    #
    # plt.xlabel("$k$")
    # plt.ylabel("$p(k)$")
    # plt.show()


