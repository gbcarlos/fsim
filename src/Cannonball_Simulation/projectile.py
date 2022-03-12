# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 15:28:18 2022

@author: Carlos
"""
import pygame

class projectile(object):
    def __init__(self,coords,color,vel=0, mv=False):
        self.origin = coords
        self.x = coords[0]
        self.y = coords[1]
        self.radius = 8
        self.color = color
        self.vel = vel # Hierüber evtl steuern wie schnell sich der ball bewegt
        self.move = mv

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        
    def respawn(self):
        self.x = self.origin[0]
        self.y = self.origin[1]