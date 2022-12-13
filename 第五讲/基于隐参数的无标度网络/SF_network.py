#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/4/9 0:23
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
from bisect import bisect


# 定义求度分布的函数
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



if __name__ == '__main__':
    N = 5000
    gamma = 2.1
    avk = 6.0
    L = int(avk*N/2)

    G = generate_SF_network(N, gamma, L)
    k, Pk = get_pdf(G)

    plt.figure(figsize=(6, 4.8))
    plt.plot(k, Pk, 'ro-')
    plt.xlabel("$k$")
    plt.ylabel("$p_k$")
    plt.xscale("log")
    plt.yscale("log")
    plt.tight_layout()
    plt.show()


