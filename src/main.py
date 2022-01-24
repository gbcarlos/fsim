import pygame
import math
import numpy as np

pygame.init()

win_size = (500,480)
win = pygame.display.set_mode(win_size)

pygame.display.set_caption("First Game")
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

#SETUP
g = 9.881 #meters per square seconds
x0 = 20 #meters
y0 = 80 #meters
v0 = 8 #meters per second
alpha = 45 #degrees

py_origin = coord_trafo_pygame([x0,y0], win_size[1])
                
class projectile(object):
    def __init__(self,coords,radius,color,vel=0):
        self.origin = coords
        self.x = coords[0]
        self.y = coords[1]
        self.radius = radius
        self.color = color
        self.vel = vel

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        
    def respawn(self):
        self.x = self.origin[0]
        self.y = self.origin[1]

def parabelBahn(t):
    coords = np.array((2,1))
    coords[0] = v0 * math.cos(alpha) * t + x0
    coords[1] = v0 * math.sin(alpha) * t + y0 - 0.5 * g * np.square(t)
    return coords

def coord_trafo_pygame(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left).
    Input: coords = [x,y], height = height of window"""
    return (coords[0], height - coords[1])

def redrawGameWindow():
    win.blit(bg, (0,0))
    bullets.draw(win)
    pygame.display.update()


#mainloop
bullets = projectile(py_origin, 6, (0,0,0))
start_time = 0
run = True
while run:
    clock.tick(160)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        start_time = pygame.time.get_ticks()
        bullets.respawn()
        bullets.vel = 8
    
    if bullets.x < win_size[0] and bullets.y < win_size[1]:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 #in seconds
        coords = parabelBahn(elapsed_time)
        coords_py = coord_trafo_pygame(coords, win_size[1])
        bullets.x = coords_py[0]
        bullets.y = coords_py[1]
    
    redrawGameWindow()

pygame.quit()







