#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/4/23 20:26

import random
import networkx as nx
import numpy as np
from bisect import bisect

# 定义求度分布的函数：获取各个不同度值对应的概率（适用于网络节点数量比较少的情况）
def get_pdf(G):
    all_k = [G.degree(i) for i in G.nodes()]
    k = list(set(all_k))  # 获取所有可能的度值
    N = len(G.nodes())

    Pk = []
    for ki in sorted(k):
        c = 0
        for i in G.nodes():
            if G.degree(i) == ki:
                c += 1
        Pk.append(c / N)

    return sorted(k), Pk

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


# 模型A：新节点与旧节点随机相连（随机增长模型）
def model_A(n0, n, m):
    # 假定初始网络是一个包含n0个节点的完全网络
    G = nx.complete_graph(n0)
    targets = list(range(m))

    repeated_nodes = list(range(n0))

    source = n0
    while source < n:
        G.add_edges_from(zip([source] * m, targets))
        # repeated_nodes.extend(targets)
        repeated_nodes.extend([source])
        targets = random.sample(repeated_nodes, m)
        # targets = set(targets)
        # while len(targets) < m:
        #     x = random.choice(repeated_nodes)
        #     targets.add(x)
        source += 1
    return G


# 非线性偏好连接模型
def generate_nonlinear_preferential(n0, n, m, alpha):
    # 假定初始网络是一个包含n0个节点的完全网络
    G = nx.complete_graph(n0)

    # 计算累计概率
    for i in range(n0, n):
        # 计算已经存在于网络中节点的度的alpha次方
        kj_alpha = np.array([G.degree(j) for j in G.nodes()]) ** alpha
        nom_kj_alpha = kj_alpha/np.sum(kj_alpha)
        # 计算累积概率分布
        nt = len(G.nodes())
        # print(nom_kj_alpha)

        # random.shuffle(nom_kj_alpha)
        cum_kj = np.array([np.sum(nom_kj_alpha[:i]) for i in range(nt)])
        # print(cum_kj)

        c = 0
        while c < m:
            r = random.random()
            j = bisect(cum_kj, r) - 1
            e1 = (i, j)
            e2 = (j, i)
            if e1 not in G.edges() or e2 not in G.edges():
                G.add_edge(*e1)
                c += 1

        G.add_node(i)
    return G