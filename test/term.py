#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pygame

from pygame.locals import *
from game.mechanics.term.Term import Term

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    os.chdir("../")
    screen = pygame.display.set_mode((900, 900))
    term = Term("test-user", "localhost", (900, 900))

    while True:
        screen.blit(term.get_surface(), (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                term.keydown(event.key)
