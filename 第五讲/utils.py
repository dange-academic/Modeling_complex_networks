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