#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/4/8 0:47

import matplotlib.pyplot as plt
import igraph as ig


# 定义求度分布的函数
def get_pdf(G):
    all_k = G.degree()
    k = list(set(all_k))  # 获取所有可能的度值
    N = len(all_k)

    Pk = []
    for ki in sorted(k):
        c = 0
        for i in G.vs:
            if G.degree(i) == ki:
                c += 1
        Pk.append(c / N)

    return sorted(k), Pk


if __name__ == '__main__':
    N = 5000
    avk = 6.0
    L = int(avk*N/2)
    gamma = 2.1

    G = ig.Graph.Static_Power_Law(N, L, gamma)
    k, Pk = get_pdf(G)

    plt.figure(figsize=(6, 4.8))
    plt.plot(k, Pk, 'ro-')
    plt.xlabel("$k$")
    plt.ylabel("$p_k$")
    plt.xscale("log")
    plt.yscale("log")

    plt.show()





