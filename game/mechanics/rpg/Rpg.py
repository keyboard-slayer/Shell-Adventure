import pygame
from typing import Tuple

class Rpg:
    def __init__(self, size):
        self.sprites = {}
        self.surface = pygame.Surface(size)

    def add_to_surface(self, name: str, sprite: pygame.sprite.Sprite, pos: Tuple[int, int]):
        self.sprites[name] = [sprite, pos]

    def get_surface(self) -> pygame.Surface:
        self.update()
        return self.surface

    def update(self):
        self.surface.fill((0, 255, 0))
        for sprite in self.sprites.values():
            self.surface.blit(sprite[0].get_surface(), sprite[1])

    def resize(self, size):
        self.surface = pygame.Surface(size)
        