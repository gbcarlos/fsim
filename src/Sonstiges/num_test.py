# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:16:00 2022

@author: Carlos
"""

from math import sin, cos
import matplotlib.pyplot as plt
import numpy as np

def euler (f, x0, y0, h, n):
    x = x0
    y = y0
    result = [(x, y)]
    for i in range(n):
        x += h
        y += h * f(x,y)
        result.append((x, y))
    return result

P = euler(lambda x, y: -sin(x), 0, 1, 0.1, 40)

plt.figure()

plt.plot(*zip(*P), '--')
x = np.linspace(0, 4, 20)
plt.plot(x, np.cos(x))

plt.show()