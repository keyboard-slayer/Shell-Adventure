#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *
from game.mechanics.term.Term import Term
from game.mechanics.quest.Quest import Quest
from game.lang.Interpreter import Interpreter


def launchGame():
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    mono = pygame.font.Font("font/monospace.ttf", 22)
    display = pygame.display.set_mode((1920, 1080))

    term = Term("test-user", "localhost", (500, 540), font=mono)
    quest = Quest((500, 540), font=mono)

    pygame.draw.rect(display, (0, 255, 0), (0, 0, 1420, 1080))  #  Jeu principal -> Vive le rpg

    lang = Interpreter(term, quest)
    lang.execute("test-wait.adv")

    while True:
        display.blit(term.get_surface(), (1420, 0))
        display.blit(quest.get_surface(), (1420, 540))
        lang.mainloop()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                term.keydown(event.key)
