#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pygame

from typing import Tuple

class Dialog:
    def __init__(self, icon: str, txt: str, color: Tuple[int, int, int], screenSize: Tuple[int, int], font=None, haveToContinue=False):
        if font is None:
            self.font = pygame.font.Font("../font/monospace.ttf", 22)
        else:
            self.font = pygame.font.Font(font, 22)
        
        self.surface = pygame.Surface((screenSize[0], 125))
        self.haveToContinue = haveToContinue
        
        self.txt = txt
        self.screenHeight = screenSize[1]

        if not os.path.isfile(icon):
            raise Exception(f"The file {icon} is not found")
        

        self.img = pygame.image.load(icon)
        self.img.set_colorkey(color)

    def update(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(
            self.font.render(
                self.txt,
                True,
                (255, 255, 255)
            ), (100, 35)
        )

        if self.haveToContinue:
            self.surface.blit(
                self.font.render(
                    "-›",
                    True,
                    (255, 255, 255)
                ), (0, 0)
            )

        self.surface.blit(self.img, (0, 35))


    def get_surface(self):
        self.update()
        return self.surface

    def get_pos(self):
        return (0, self.screenHeight-180) # NOTE: permet de faciliter la programmation de l'objet RPG

    def keydown(self, keydown):
        if keydown == 13: # == K_RETURN
            return "del self.sprites['dialog']"