import pygame
from typing import Tuple

class Rpg:
    def __init__(self, size):
        self.sprites = {}
        self.surface = pygame.Surface(size)

    def add_to_surface(self, name: str, sprite: pygame.sprite.Sprite):
        self.sprites[name] = sprite

    def get_surface(self) -> pygame.Surface:
        self.update()
        return self.surface

    def update(self):
        self.surface.fill((0, 255, 0))
        for sprite in self.sprites.values():
            self.surface.blit(sprite.get_surface(), sprite.get_pos())

    def resize(self, size: Tuple[int, int]):
        self.surface = pygame.Surface(size)

        