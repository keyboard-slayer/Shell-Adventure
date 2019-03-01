#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pygame

from typing import Tuple

class Dialog:
    def __init__(self, icon: str, txt: str, color: Tuple[int, int, int], font=None, size=(1920, 50), pos=(0, 1030)):
        if font is None:
            font = pygame.font.Font("./font/monospace.ttf", 22)
        
        self.font = font
        self.pos = pos
        self.surface = pygame.Surface((size))
        self.txt = txt

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
            ), (0, 0)
        )


    def get_surface(self):
        self.update()
        return self.surface

    def get_pos(self):
        return self.pos