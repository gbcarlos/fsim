# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:20:45 2022

@author: Carlos
"""

import pygame

BLACK = (0, 0, 0)

class TextInput:
    
    _threshold = 70 #static variable for handling of multiple text inputs in one menu
    
    def __init__(self, menu_width, text='', label='', unit=''):
        pygame.font.init()
        
        self.menu_width = menu_width
        self.base_font = pygame.font.SysFont('Calibri', 20)
        self.user_text = text
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False #checks if text field is selected
        self.rect_size = (80, 32)
        self.rect_pos = (self.menu_width / 2 - self.rect_size[0] / 2, TextInput._threshold)
        self.input_rect = pygame.Rect(
                self.rect_pos[0],
                self.rect_pos[1],
                self.rect_size[0],
                self.rect_size[1])
        
        self.label = label
        self.unit = unit
        
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
                if len(self.user_text) > 1:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text = u"0"
                    
            elif self.active and event.key != pygame.K_SPACE and event.key != pygame.K_RETURN and event.key != pygame.K_TAB:
                # adds sign from event
                self.user_text += event.unicode
                
                if self.user_text[0] == "0":
                    self.user_text = self.user_text[1:]

    def draw(self, win):
        # Draws input rectangle on menu and text into 
        pygame.draw.rect(win, self.color, self.input_rect)
        
        # Creates Surface and rect for the text input of user, label and unit
        text_surface = self.base_font.render(self.user_text, True, BLACK)
        text_rect = text_surface.get_rect()
        
        label_surface = self.base_font.render(self.label, True, BLACK)
        label_rect = label_surface.get_rect()
        
        unit_surface = self.base_font.render(self.unit, True, BLACK)
        unit_rect = unit_surface.get_rect()
        
        # Centers the text field, label and unit
        text_rect.center = (self.rect_pos[0] + self.rect_size[0] / 2, self.rect_pos[1] + self.rect_size[1] / 2)
        label_rect.center = (0.25 * self.menu_width, self.rect_pos[1] + self.rect_size[1] / 2)
        unit_rect.center = (0.75 * self.menu_width, self.rect_pos[1] + self.rect_size[1] / 2)
        
        # Blits everything on win (menu screen)
        win.blit(text_surface, text_rect) #[self.input_rect.x, self.input_rect.y])
        win.blit(label_surface, label_rect)
        win.blit(unit_surface, unit_rect)
        
        
        
        
        
        