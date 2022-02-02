# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:20:45 2022

@author: Carlos
"""

import pygame
import sys

class TextInput:
    def __init__(self):
        pygame.font.init()

        self.base_font = pygame.font.SysFont('Calibri', 32)
        self.user_text = ''
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        
        self.input_rect = pygame.Rect(200, 200, 140, 32)
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.input_rect)