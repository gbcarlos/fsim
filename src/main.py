'''
Cannonball Simulation
'''
#Imports
from functions import parabelBahn, coord_trafo_pygame, redrawGameWindow
from projectile import projectile

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

#mainloop
bullet = projectile(py_origin, 6, (0,0,0))
start_time = 0
run = True

while run:
    clock.tick(220)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        start_time = pygame.time.get_ticks()
        bullet.respawn()
        bullet.move = True
        bullet.vel = 8
    
    if bullet.x < win_size[0] and bullet.y < win_size[1] and bullet.move:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 #in seconds
        coords = parabelBahn(elapsed_time, v0, g, alpha, x0, y0)
        coords_py = coord_trafo_pygame(coords, win_size[1])
        bullet.x = coords_py[0]
        bullet.y = coords_py[1]
    
    redrawGameWindow(win, bg, bullet)

pygame.quit()







