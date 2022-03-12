import pygame
import sys
from TextInput import TextInput

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600, 500])

ti = TextInput()

while True:
    for event in pygame.event.get():

    # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        ti.check_userInput(event)
        
    ti.draw(screen)

    pygame.display.flip()
    
    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)
pygame.quit()

