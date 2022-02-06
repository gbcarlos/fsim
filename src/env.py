# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:35:16 2022

@author: Carlos
"""

import pygame
from button import Button
from TextInput import TextInput

# COLORS
BEIGE = (249,228,183)
BLACK = (0,0,0)

# Settings for environment:
METER_TO_PIXEL = 100  # Factor to scale playground between pixel and meters (default drone size is ~0.3m)

class Environment:
    def __init__(self):
        # SETUP PYGAME
        pygame.init()
        self.m_to_pxl = METER_TO_PIXEL
        self.clock = pygame.time.Clock()       
        
        # MAIN SCREEN
        pygame.display.set_caption("Cannonball Simulation")
        self.win_size = (1100,480)
        self.main_screen = pygame.display.set_mode(self.win_size) # SURFACE main_screen = menu + sim
        
        # MENU SCREEN
        self.menu_width = 300
        self.menu_coord = self.menu_width / 2
        self.menu_screen = pygame.Surface((self.menu_width, self.win_size[1]))
        self.menu_screen.fill(BEIGE)
        
        # MENU DESIGN
        self.display_text("Simulation Parameters",(self.menu_width / 2, 50), fontsize=20, under_line=True, bold=True)
        self.ti_gravity = TextInput(self.menu_width, "9.881", label="g", unit="[m/s^2]")
        self.ti_x0 = TextInput(self.menu_width, "20", label="x0", unit="[m]")
        self.ti_y0 = TextInput(self.menu_width, "80", label="y0", unit="[m]")
        self.ti_v0 = TextInput(self.menu_width, "60", label="v0", unit="[m/s]")
        self.ti_alpha = TextInput(self.menu_width, "45", label="Alpha", unit="[deg]")
        
        
        # SIMULATION SCREEN
        self.sim_screen_width = self.win_size[0] - self.menu_width
        self.sim_screen_coord = self.menu_width + self.sim_screen_width / 2
        self.sim_screen = pygame.Surface((self.sim_screen_width, self.win_size[1]))
        self.bg = pygame.image.load('bg.jpg')
        
        # INITIALIZE SCREENS
        '''
        Blit the background image on the simulation surface,
        then blit menu and simulation surface on main screen
        '''
        self.sim_screen.blit(self.bg, (0, 0))
        self.main_screen.blit(self.menu_screen, (0,0))
        self.main_screen.blit(self.sim_screen, (self.menu_width, 0))
        
        
    def display_text(self, text: str, pos, fontsize: int = 16, align: str = 'center', under_line=False, bold=False) -> None:
        '''
        Function to create text with coordinates given in center!

        :param align: left or center alignment
        :param text: Text to display
        :param pos: center or left position of text
        :param fontsize: fontsize number (only change of necessary, causes too much lag otherwise)
        :param under_line: Decide if text should be underlined
        '''
    
        my_font = pygame.font.SysFont('Arial', fontsize, bold=bold)
        
        if under_line:
            my_font.set_underline(True)
            
        text_surface = my_font.render(text, False, BLACK)
        text_rect = text_surface.get_rect()
        
        if align == 'center':
            text_rect.center = pos
        else:
            text_rect.midleft = pos
            
        self.menu_screen.blit(text_surface, text_rect)   
