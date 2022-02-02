# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:20:45 2022

@author: Carlos
"""

import pygame

BLACK = (255, 255, 255)

class TextInput:
    
    _threshold = 70 #static variable
    
    def __init__(self, menu_width, text=''):
        pygame.font.init()
        
        self.base_font = pygame.font.SysFont('Calibri', 22)
        self.user_text = text
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False #checks if text field is selected
        self.rect_size = (80, 32)
        self.rect_pos = (menu_width / 2 - self.rect_size[0] / 2, TextInput._threshold)
        self.input_rect = pygame.Rect(
                self.rect_pos[0],
                self.rect_pos[1],
                self.rect_size[0],
                self.rect_size[1])
        
        TextInput._threshold += 50 #counts up for each new instance created, assures structure of menu
        
    def check_userInput(self, event):
        '''
        Checks for user input:
            if mouse is clicked:
                checks if text field is selected
            if key is pressed:
                checks if text field is selected AND
                checks if signs are added or deleted from text field
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_passive

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_BACKSPACE and self.active:

                # deletes last letter/number
                self.user_text = self.user_text[:-1]

            elif self.active:
                # adds sign from event
                self.user_text += event.unicode
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.input_rect)
        text_surface = self.base_font.render(self.user_text, True, BLACK)
        #text_rect = text_surface.get_rect()
        #text_rect.center = (self.rect_size[0] / 2, self.rect_size[1] / 2)
        win.blit(text_surface, text_rect) #(self.input_rect.x, self.input_rect.y)
        #win.blit(text_rect)