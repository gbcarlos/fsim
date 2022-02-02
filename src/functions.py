# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 15:27:23 2022

@author: Carlos
"""
import numpy as np
import math
import pygame

def parabelBahn(t, v0, g, alpha, x0, y0):
    coords = np.array((2,1))
    coords[0] = v0 * math.cos(alpha) * t + x0
    coords[1] = v0 * math.sin(alpha) * t + y0 - 0.5 * g * np.square(t)
    return coords

def coord_trafo_pygame(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left).
    Input: 
        coords = [x,y],
        width = width of the menu (0,0 starts in simulation window),
        height = height of window (will be reversed)
    """
    return (coords[0], height - coords[1])