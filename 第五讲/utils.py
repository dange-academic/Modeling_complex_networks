#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/4/9 0:23

import numpy as np
import math
import random
import networkx as nx
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
        Pk.append(c/N)     
    
    return sorted(k), Pk


# 二分查找函数
def bisection_search(array, a):
    n = len(array)
    jl = 0
    ju = n-1
    flag = (array[n-1]>=array[0]) # 判断array数组是否为升序排序
    while ju-jl > 1:
        jm = math.ceil((ju+jl)/2)
        if (a > array[jm]) == flag:
            jl = jm
        else:
            ju = jm

    if a == array[0]:
        j = 1
    elif a == array[n-1]:
        j = n-2
    else:
        j = jl + 1

    return j

# 隐参数模型生成无标度网络
def generate_SF_network(N, gamma, L):
    alpha = 1 / (gamma - 1)
    n = np.linspace(1, N, N)
    eta = n ** (-alpha)
    nom_eta = eta / np.sum(eta)
    random.shuffle(nom_eta)
    cum_eta = np.array([np.sum(nom_eta[:i]) for i in range(N)])
    edges = []

    c = 0
    while c < L:
        # i = bisection_search(cum_eta, np.random.rand(2)[0])
        # j = bisection_search(cum_eta, np.random.rand(2)[1])
        i = bisect(cum_eta, np.random.rand(2)[0])
        j = bisect(cum_eta, np.random.rand(2)[1])
        if i == j:
            continue
        e1 = (i, j)
        e2 = (j, i)
        if e1 not in edges and e2 not in edges:
            edges.append(e1)
            c += 1

    G = nx.Graph()
    G.add_edges_from(edges)

    return G


# 定义求距离分布的函数
def get_pdf_spl(G):
    nodes = list(G.nodes())
    n = len(nodes)
    # 计算所有节点对之间的最短距离会很慢
    # all_spl = [nx.shortest_path_length(G, nodes[i], nodes[j]) for i in range(len(nodes)-1)
    #            for j in range(i+1,len(nodes)) if nx.has_path(G, nodes[i], nodes[j])]
    
    all_spl = []
    samples = int(0.1*n*(n-1)/2)
    m = 0
    while m < samples:
        i = random.choice(nodes)
        j = random.choice(nodes)
        if i == j:
            continue
        if nx.has_path(G, i, j):
            all_spl.append(nx.shortest_path_length(G, i, j))
            m += 1
            
    spl = list(set(all_spl)) # 所有可能的距离值

    Pl = []
    for spli in sorted(spl):
        c = 0
        for i in range(len(all_spl)):
            if all_spl[i] == spli:  
                c += 1  

        Pl.append(c/len(all_spl))     
    
    return sorted(spl), Pl


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