# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:33:53 2022

@author: Carlos
"""

import numpy as np
import math

class Simulation:
    def __init__(self, sim_screen_size):

        self.sim_screen_size = sim_screen_size
        self.start_time = 0  # sec
        self.elapsed_time = 0  # sec
        self.h = 0.01  # time step width
        self.curr_time_step = 0
        self.sim_time = 0.0  # time used for calculation of new values

        # SIMULATION PARAMETERS

        self.gravity = 9.881 #m/s^2
        self.x0 = 20 #m
        self.y0 = 80 #m
        self.v0 = 60 #m/s
        self.alpha = 45 #deg

        # SIMULATION WITHOUT NUMERICAL ALGORITHM

        self.pos = np.array((2,1)) #Current position of cannonball

        # SIMULATION WITH SELECTED ALGORITHM
        self.pos_alg = np.array((2,1))
        self.vel_alg = np.array((2,1))
        self.acc_alg = np.array((0, self.gravity))
        
    def sim2py(self, coords):
        '''
        Convert coordinates into pygame coordinates (lower-left => top left).
        Input: 
        coords = [x,y],
        width = width of the menu (0,0 starts in simulation window),
        height = sim_screen_size[1], height of window (will be reversed)
        '''
        
        return [coords[0], self.sim_screen_size[1] - coords[1]]

    def py2sim(self, coords):

        return [coords[0], self.sim_screen_size[1] - coords[1]]

    def getOrigin(self):
        '''
        Returns origin of the cannonball
        '''
        return self.sim2py([self.x0, self.y0])

    def init_alg(self):
        '''
        Inits the values for the selected algorithm
        '''
        self.acc_alg = np.array((0, self.gravity))
        self.vel_alg = np.array((self.v0 * math.cos(np.deg2rad(self.alpha)), self.v0 * math.cos(np.deg2rad(self.alpha))))
        self.pos_alg = np.array((self.x0, self.y0))

    def update_simTime(self, new_time):
        '''
        Updates the elapsed time within simulation (seconds)
        for new calculation of position
        '''
        self.elapsed_time = new_time / 1000 - self.start_time
        
    def update_pos(self, algorithm=0):
        '''
        Updates self.pos with new time step and given algorithm or eom
        and converts into pygame coordinates
        '''

        if algorithm == 1:
            # Euler selected

            # Calculate velocities using accelerations
            #self.vel_alg[0] = self.euler(self.vel_alg[0], self.acc_alg[0])
            self.vel_alg[1] = self.euler(self.vel_alg[1], self.acc_alg[1])

            # Calculate position using velocities
            #self.pos_alg[0] = self.euler(self.pos_alg[0], self.vel_alg[0])
            #OR:
            self.pos_alg[0] += self.h
            self.pos_alg[1] = self.euler(self.pos_alg[1], self.vel_alg[1])

        elif algorithm == 2:
            # Trapez selected
            pass

        else:
            # No algorithm selected in dropdown or error
            self.eom()
            self.pos = self.sim2py(self.pos)

    def eom(self):
        '''
        Equation of motion of cannonball (can be solved analytically)
        Is used here for comparison to numerical solutions
        '''

        self.pos[0] = self.v0 * math.cos(np.deg2rad(self.alpha)) * self.sim_time + self.x0
        self.pos[1] = self.v0 * math.sin(np.deg2rad(self.alpha)) * self.sim_time + self.y0 - 0.5 * self.gravity * np.square(self.sim_time)

    def euler(self, y_old, x):
        return y_old + h * x
    
    def trapez(self):
        #y_new = y_old + h*
        #return y_new
        pass

    def modRK(self):
        pass