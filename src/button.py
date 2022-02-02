# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:39:03 2022

@author: Carlos
"""

class Button:
    def __init__(self, environment, color, x, y, width, height, text='', fontsize=30):
        self.env = environment
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fontsize = fontsize

    def draw(self, outline=True):
        """
        Call to draw Button with text given during creation

        :param outline: Whether button should have black outline
        """
        if outline:
            pygame.draw.rect(self.env.screen,
                             self.env.BLACK,
                             (self.x - self.width/2 - 2, self.y - self.height/2 - 2, self.width + 4, self.height + 4),
                             0)

        pygame.draw.rect(self.env.screen,
                         self.color,
                         (self.x - self.width/2, self.y - self.height/2, self.width, self.height),
                         0)

        if self.text != '':
            font = pygame.font.SysFont('Comic Sans MS', self.fontsize)
            text_surface = font.render(self.text, True, self.env.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (self.x, self.y)
            self.env.screen.blit(text_surface, text_rect)

    def is_over(self, pos):
        """
        Function to check, whether mouse position is over button position

        :param pos: mouse position
        :return:
        """
        if self.x - self.width/2 < pos[0] < self.x + self.width/2:
            if self.y - self.height/2 < pos[1] < self.y + self.height/2:
                return True
        return False
