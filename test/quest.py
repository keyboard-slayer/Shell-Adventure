#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pygame

from game.mechanics.quest.Quest import Quest

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    os.chdir("../")
    screen = pygame.display.set_mode((900, 900))
    quest = Quest((900, 900))
    quest.add("Ceci est un test")
    while True:
        screen.blit(quest.get_surface(), (0, 0))
        pygame.display.flip()
