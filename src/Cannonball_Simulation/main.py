'''
Cannonball Simulation by Carlos
'''
# IMPORTS
import pygame
from projectile import projectile
from env import Environment
from sim import Simulation

BLACK = (0,0,0)

# INITIALISATION
env = Environment()
sim = Simulation(env.win_size)

sim_origin = sim.getOrigin()
cball = projectile(sim_origin, BLACK)
run = True

# MAIN LOOP
while run:
    env.clock.tick(60)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        
        # Graphical Updates by user text inputs
        env.check4userUpdates(event)

        # Read out DropDown selection
        sel_algorithm = env.algorithm_dropdown.update(event)

        # Check if simulation button has been pressed
        env.sim_button.handleEvent(event)

        # If pressed, setup and start simulation
        if env.sim_button.buttonDown:

            # Update Sim Parameters with user input
            sim.gravity = float(env.ti_gravity.user_text)
            sim.x0 = float(env.ti_x0.user_text)
            sim.y0 = float(env.ti_y0.user_text)
            sim.v0 = float(env.ti_v0.user_text)
            sim.alpha = float(env.ti_alpha.user_text)

            # Start the simulation
            sim.sim_time = 0.0
            sim.curr_time_step = 0
            sim.init_alg()
            sim.start_time = pygame.time.get_ticks() / 1000 # in sec
            cball.respawn()
            cball.move = True

    # Executed when simulation is still running and ball is not outside window    
    if cball.x < env.win_size[0] and cball.y < env.win_size[1] and cball.move:

        # Update Step time & position of cannonball using numerical algorithm
        sim.sim_time += 0.1#sim.h h != time step
        sim.curr_time_step += 1
        sim.update_simTime(pygame.time.get_ticks())
        sim.update_pos(sel_algorithm)

        # Assign new position to cannonball
        if sel_algorithm > 0:
            cball.x = sim.pos_alg[0]
            cball.y = sim.pos_alg[1]
        else:
            cball.x = sim.pos[0]
            cball.y = sim.pos[1]

        print("Time: %2.2f Position: %8.2f %8.2f \n" % (sim.curr_time_step, sim.py2sim(sim.pos)[0], sim.py2sim(sim.pos)[1]))

    ### SCREEN UPDATES ###
    
    # Update cannonball position on sim_screen and show simtime on sim_screen
    env.sim_screen.blit(env.bg, (0, 0))
    cball.draw(env.sim_screen)

    # Print out simulation uptime and sim time on sim screen
    font = pygame.font.Font(None, 25)
    min = int(sim.elapsed_time // 60)
    sec = int(sim.elapsed_time % 60)
    output_string = "Uptime: {0:02}:{1:02}".format(min, sec)
    text_time = font.render(output_string, True, BLACK)
    env.sim_screen.blit(text_time, [40, 40])

    output2 = "Current time step: {0:02}".format(sim.curr_time_step)
    text_timestep = font.render(output2, True, BLACK)
    env.sim_screen.blit(text_timestep, [40, 55])

    # Update text fields with user inputs on menu_screen
    env.update_Menu()

    # Update main_screen
    env.main_screen.blit(env.sim_screen, (env.menu_width, 0))
    env.main_screen.blit(env.menu_screen, (0, 0))
    
    pygame.display.update()

pygame.quit()






