import pygame
from pygame.locals import *

from typing import (
    Tuple,
    Dict
)


class Rpg:
    def __init__(self, size):
        self.sprites = {}
        self.surface = pygame.Surface(size)
        self.mouseCollide = False
        self.interruption = False

    def get_interruption(self) -> bool:
        return not self.interruption

    def clear(self):
        self.surface.fill((0, 255, 0))

    def add_to_surface(self, name: str, sprite: pygame.sprite.Sprite):
        self.sprites[name] = sprite

    def in_surface(self) -> Dict[str, object]:
        return self.sprites

    def did_mouse_collide(self) -> bool:
        return self.mouseCollide

    def set_mouse_collide(self, collide: bool):
        self.mouseCollide = collide

    def get_surface(self) -> pygame.Surface:
        self.update()
        return self.surface

    def get_size(self) -> Tuple[int, int]:
        return self.surface.get_size()

    def update(self):
        self.clear()
        for sprite in self.sprites.values():
            self.surface.blit(sprite.get_surface(), sprite.get_pos())

    def resize(self, size: Tuple[int, int]):
        self.surface = pygame.Surface(size)

    def keydown(self, key: int):
        instructions = []
        if self.mouseCollide:
            for sprite in self.sprites.values():
                try:
                    awnser = sprite.keydown(key)
                    if awnser:
                        instructions.append(awnser)
                except AttributeError:
                    continue

        for instrct in instructions:
            exec(instrct)
