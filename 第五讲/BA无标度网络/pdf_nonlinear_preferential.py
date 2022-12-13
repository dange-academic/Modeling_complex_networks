#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： 单哥的科研日常
# Time ： 2022/4/23 20:26

from utils import *
import powerlaw
import matplotlib.pyplot as plt


n0 = 3
n = 10000
m = 2
alpha1 = 0.5
alpha2 = 1.0
alpha3 = 1.5

G1 = generate_nonlinear_preferential(n0, n, m, alpha1)
G2 = generate_nonlinear_preferential(n0, n, m, alpha2)
G3 = generate_nonlinear_preferential(n0, n, m, alpha3)
degree_seq1 = [G1.degree(i) for i in G1.nodes()]
degree_seq2 = [G2.degree(i) for i in G2.nodes()]
degree_seq3 = [G3.degree(i) for i in G3.nodes()]

print("===========")
# 对数坐标，对数分箱
# powerlaw.plot_pdf(degree_seq1, linear_bins = False, color = 'r', marker='o', label=r'$\alpha = 0.5$')
# powerlaw.plot_pdf(degree_seq2, linear_bins = False, color = 'b', marker='s', label=r'$\alpha = 1.0$')
# powerlaw.plot_pdf(degree_seq3, linear_bins = False, color = 'g', marker='v', label=r'$\alpha = 1.5$')


k1, pk1 = get_pdf(G1)
k2, pk2 = get_pdf(G2)
k3, pk3 = get_pdf(G3)
plt.plot(k1, pk1, "ro", label=r'$\alpha = 0.5$')
plt.plot(k2, pk2, "bs", label=r'$\alpha = 1.0$')
plt.plot(k3, pk3, "gv", label=r'$\alpha = 1.5$')
plt.legend(loc=0)
plt.xscale("log")
plt.yscale("log")
plt.xlim([1,1e4])
plt.xlabel("$k$")
plt.ylabel("$p(k)$")
plt.show()