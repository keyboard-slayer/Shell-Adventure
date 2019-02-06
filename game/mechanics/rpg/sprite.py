#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame 

from typing import Tuple 

class Sprite():
    def __init__(self, imgFile: str, color: Tuple[int, int, int], size: Tuple[int, int], nbr: int, finalSize: Tuple[int, int]):
        self.size = size
        self.finalSize = finalSize
        self.index = (0, 0) # X Y (Max (4, 4))
        try:
            self.spriteSurface = pygame.Surface(size, pygame.SRCALPHA)
            self.spriteSurface.set_alpha(255)
            self.spriteSheet = pygame.image.load(imgFile).convert()
        except pygame.error:
            raise Exception(f"Image {imgFile} not found")
        
        self.spriteSheet.set_colorkey(color)
    
    def get_surface(self) -> pygame.Surface:
        self.spriteSurface.fill(pygame.SRCALPHA)
        self.spriteSurface.set_alpha(255)
        self.spriteSurface.blit(self.spriteSheet, (0, 0), (self.index[0]*self.size[0], self.index[1]*self.size[1], self.size[0], self.size[1]))
        return pygame.transform.scale(self.spriteSurface.convert_alpha(), self.finalSize)

    def reset(self, index: int):
        if self.index[0] == 3 or self.index[1] != index:
            self.index = (-1, index)

    def move(self, way: int):
        self.reset(way)
        self.index = (self.index[0]+1, way)
        print(self.index)




