# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:41:38 2022

@author: Carlos
"""

import sys, pygame, math
from pygame.locals import *

# set up a bunch of constants
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
BROWN    = (139,  69,  19)
DARKGRAY = (128, 128, 128)

BGCOLOR = BROWN

WINDOWWIDTH = 1300 # width of the program's window, in pixels
WINDOWHEIGHT = 650 # height in pixels

FPS = 30


# standard pygame setup code
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Cannonball simulation')

# create the base cannon image
cannonSurf = pygame.Surface((100, 100))
cannonSurf.fill(WHITE)
pygame.draw.circle(cannonSurf, DARKGRAY, (20, 50), 20) # left end
pygame.draw.circle(cannonSurf, DARKGRAY, (80, 50), 20) # right end
pygame.draw.rect(cannonSurf, DARKGRAY, (20, 30, 60, 40)) # body
pygame.draw.circle(cannonSurf, BLACK, (80, 50), 15) # hole
pygame.draw.circle(cannonSurf, BLACK, (80, 50), 20, 1) # right end outline
pygame.draw.circle(cannonSurf, BROWN, (30, 70), 20) # wheel
pygame.draw.circle(cannonSurf, BLACK, (30, 70), 20, 1) # wheel outline

# cannon ball image
cannonBall = pygame.Surface((28, 28))
cannonBall.fill(WHITE)
pygame.draw.circle(cannonBall, BLACK, (0,0), 14)

def getAngle(x1, y1, x2, y2):
    # Return value is 0 for right, 90 for up, 180 for left, and 270 for down (and all values between 0 and 360)
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise) # get the angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360 # adjust for a right-facing sprite
    return angle


# main application loop
while True:
    # event handling loop for quit events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # fill the screen to draw from a blank state
    DISPLAYSURF.fill(BGCOLOR)

    # draw the cannon pointed at the mouse cursor
    mousex, mousey = pygame.mouse.get_pos()
    cannon_pos = (50,600)

    degrees = getAngle(cannon_pos[0], cannon_pos[1], mousex, mousey)
    
    # rotate a copy of the cannon image and draw it
    rotatedSurf = pygame.transform.rotate(cannonSurf, degrees)
    #rotatedRect = rotatedSurf.get_rect()
    #rotatedRect.center = (cannon_pos[0], cannon_pos[1])
    
    # rotate cannonball too
    #rotatedBall = pygame.transform.rotate(cannonBall, degrees)
    #rotatedBallRect = rotatedBall.get_rect()
    #rotatedBallRect.center = (cannon_pos[0], cannon_pos[1])
    
    DISPLAYSURF.blit(rotatedSurf, (0,500))
    #DISPLAYSURF.blit(rotatedBall, rotatedBallRect)

    # Fadenkreuz
    pygame.draw.line(DISPLAYSURF, BLACK, (mousex - 10, mousey), (mousex + 10, mousey))
    pygame.draw.line(DISPLAYSURF, BLACK, (mousex, mousey - 10), (mousex, mousey + 10))

    # draw the border
    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT), 1)

    pygame.display.update()
    FPSCLOCK.tick(FPS)