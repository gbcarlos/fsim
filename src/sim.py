# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:33:53 2022

@author: Carlos
"""

import numpy as np
import math
import pygame

class Simulation:
    def __init__(self, sim_screen_size):
        self.gravity = 9.881 #m/s^2
        self.x0 = 20 #m
        self.y0 = 80 #m
        self.v0 = 60 #m/s
        self.alpha = 45 #deg
        self.pos = np.array((2,1)) #Current position of cannonball
        
        self.sim_screen_size = sim_screen_size
        self.start_time = 0 #sec
        self.elapsed_time = 0 #sec
        
    def sim2py(self, coords):
        '''
        Convert coordinates into pygame coordinates (lower-left => top left).
        Input: 
        coords = [x,y],
        width = width of the menu (0,0 starts in simulation window),
        height = sim_screen_size[1], height of window (will be reversed)
        '''
        
        return [coords[0], self.sim_screen_size[1] - coords[1]]
    
    def getOrigin(self):
        '''
        Returns origin of the cannonball
        '''
        return self.sim2py([self.x0, self.y0])
    
    def update_simTime(self, new_time):
        '''
        Updates the elapsed time within simulation (seconds)
        for new calculation of position
        '''
        self.elapsed_time = new_time / 1000 - self.start_time
        
    def update_pos(self):
        '''
        Updates self.pos with new time step and given algorithm or eom
        and converts into pygame coordinates
        '''
        self.eom()
        self.pos = self.sim2py(self.pos)
    
    def eom(self):
        '''
        Equation of motion of cannonball (can be solved analytically)
        Is used here for comparison to numerical solutions
        '''
        self.pos[0] = self.v0 * math.cos(self.alpha) * self.elapsed_time + self.x0
        self.pos[1] = self.v0 * math.sin(self.alpha) * self.elapsed_time + self.y0 - 0.5 * self.gravity * np.square(self.elapsed_time)
        
    def euler(self):
        pass
    
    def trapez(self):
        pass
        