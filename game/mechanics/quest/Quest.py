#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pygame

from typing import Tuple

class Quest:
    def __init__(self, size: Tuple[int, int], font: pygame.font.Font):
        self.surface = pygame.Surface(size)
        self.mono = font
        self.quests = {}

    def add(self, var: str, event: str):
        if len(self.quests) == 18:
            raise Exception("Too much quest !")
        self.quests[var] = event

    def done(self, questVar):
        if questVar not in self.quests:
            raise NameError(f"{p.NAME} is not declared")
        else:
            self.quests[questVar] = f'>{self.quests[questVar]}'

    def update(self):
        mark = False
        self.surface.fill((40, 43, 51))
        for index, quest in enumerate(self.quests.values()):
            if quest[0] == '>':
                quest = quest[1:]
                mark = True

            self.surface.blit(
                self.mono.render(
                    f"* {quest}",
                    True,
                    (255, 255, 255)
                ),
                (35, index*22+50)
            )

            if mark:
                self.surface.blit(
                    self.mono.render(
                        'OK',
                        True,
                        (0, 255, 0)
                    ),
                    (self.surface.get_size()[0]-100, index*22+50)
                )

                mark = False


    def get_surface(self):
        self.update()
        return self.surface
