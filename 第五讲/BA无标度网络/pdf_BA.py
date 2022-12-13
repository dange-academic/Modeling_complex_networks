#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/4/23 20:26

from utils import *
import powerlaw
import matplotlib.pyplot as plt


n0 = 3


# N = 100000
# m = [3,5,7]
#
#
# G1 = barabasi_albert_graph(n0, N, m[0])
# degree_seq1 = [G1.degree(i) for i in G1.nodes()]
#
# G2 = barabasi_albert_graph(n0, N, m[1])
# degree_seq2 = [G2.degree(i) for i in G2.nodes()]
#
# G3 = barabasi_albert_graph(n0, N, m[2])
# degree_seq3 = [G3.degree(i) for i in G3.nodes()]


N = [50000,100000,200000]
m = 3

G1 = barabasi_albert_graph(n0, N[0], m)
degree_seq1 = [G1.degree(i) for i in G1.nodes()]

G2 = barabasi_albert_graph(n0, N[1], m)
degree_seq2 = [G2.degree(i) for i in G2.nodes()]

G3 = barabasi_albert_graph(n0, N[2], m)
degree_seq3 = [G3.degree(i) for i in G3.nodes()]

print("===========")
# 对数坐标，对数分箱
powerlaw.plot_pdf(degree_seq1, linear_bins = False, color = 'r', marker='o', linewidth=0.0, label='$N = 50000$')
powerlaw.plot_pdf(degree_seq2, linear_bins = False, color = 'b', marker='s', linewidth=0.0, label='$N = 100000$')
powerlaw.plot_pdf(degree_seq3, linear_bins = False, color = 'g', marker='*', linewidth=0.0, label='$N = 200000$')
plt.legend(loc=0)
print("===========")

plt.xlabel("$k$")
plt.ylabel("$p(k)$")
plt.show()