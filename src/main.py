'''
Cannonball Simulation
'''
#Imports
import pygame
from functions import parabelBahn, coord_trafo_pygame
from projectile import projectile
from menu import numerical_alg, start_the_game
from env import Environment

'''
#MAIN MENU
menu = pygame_menu.Menu('Welcome', 500, 400,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='ol Doe')
menu.add.button('Change initial Parameters', start_the_game())
menu.add.selector('Num. Algorithm :', [('Euler', 1), ('Trapez', 2), ('Anderes', 3)], onchange=numerical_alg())
menu.add.button('Simulate', start_the_game())
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(win)
'''
#SETUP SIMULATION
g = 9.881 #meters per square seconds
x0 = 20 #meters
y0 = 80 #meters
v0 = 60 #meters per second
alpha = 45 #degrees


env = Environment()
py_origin = coord_trafo_pygame([x0,y0], env.win_size[1])
cball = projectile(py_origin, (0,0,0))
start_time = 0
run = True

while run:
    env.clock.tick(220)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        start_time = pygame.time.get_ticks()
        cball.respawn()
        cball.move = True
        cball.vel = 8
        
    if cball.x < env.win_size[0] and cball.y < env.win_size[1] and cball.move:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 #in seconds
        coords = parabelBahn(elapsed_time, v0, g, alpha, x0, y0)
        coords_py = coord_trafo_pygame(coords, env.win_size[1])
        cball.x = coords_py[0]
        cball.y = coords_py[1]
    
    # Draw cannonball position on sim_screen and blit sim_screen on main_screen

    env.sim_screen.blit(env.bg, (0, 0))
    cball.draw(env.sim_screen)
    env.main_screen.blit(env.sim_screen, (env.menu_width, 0))
    
    pygame.display.update()

pygame.quit()






