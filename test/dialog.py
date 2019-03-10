import os
import pygame

from game.mechanics.rpg.dialog import Dialog 
from game.mechanics.rpg.Rpg import Rpg 


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((900, 900))

    rpg = Rpg((900, 900))
<<<<<<< HEAD
    rpg.add_to_surface("dialog-sci", Dialog("../intro/sprite/dialog-sci.png", "Hello World!", color=(60, 255, 0), haveToContinue=True))
    
=======
    rpg.add_to_surface("dialog-sci", Dialog("../intro/sprite/dialog-sci.png", "Hello World!", color=(60, 255, 0), size=(900, 50), pos=(0, 850)))


>>>>>>> bac713826a8df7038cc2f4b383c0073b459b252b
    while True:
        clock.tick(60)
        rpg.update()
        display.blit(rpg.get_surface(), (0, 0))
        pygame.display.flip()