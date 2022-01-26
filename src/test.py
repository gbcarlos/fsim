# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 11:50:16 2022

@author: Carlos
"""


#Imports
import pygame
import pygame_menu
from functions import parabelBahn, coord_trafo_pygame, redrawGameWindow
from projectile import projectile
from menu import numerical_alg, start_the_game
from main import mainloop

#SETUP PYGAME 
pygame.init()
win_size = (500,480)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Cannonball Simulation")
bg = pygame.image.load('bg.jpg')
clock = pygame.time.Clock()

#SETUP SIMULATION
g = 9.881 #meters per square seconds
x0 = 20 #meters
y0 = 80 #meters
v0 = 60 #meters per second
alpha = 45 #degrees

py_origin = coord_trafo_pygame([x0,y0], win_size[1])

#MAIN MENU
menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.button('Change initial Parameters', start_the_game())
menu.add.selector('Num. Algorithm :', [('Euler', 1), ('Trapez', 2), ('Anderes')], onchange=numerical_alg())
menu.add.button('Simulate', mainloop())
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(win)

