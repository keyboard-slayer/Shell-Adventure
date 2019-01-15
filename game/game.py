#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *
from game.mechanics.term.Term import Term
# from game.mechanics.quest.Quest import Quest


def launchGame():
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    display = pygame.display.set_mode((1920, 1080))
    term = Term("test-user", "localhost", (500, 540), )
    pygame.draw.rect(display, (0, 0, 255), (1420,540, 500, 540)) # Quest -> Donnerais les quetes
    pygame.draw.rect(display, (0, 255, 0), (0, 0, 1420, 1080))  #  Jeu principal -> Vive le rpg



    while True:
        display.blit(term.get_surface(), (1420, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                term.keydown(event.key)

