import pygame

class Rpg:
    def __init__(self, size):
        self.surface = pygame.Surface(size)

    def get_surface(self) -> pygame.Surface:
        self.update()
        return self.surface

    def update(self):
        self.surface.fill((0, 255, 0))

    def resize(self, size):
        self.surface = pygame.Surface(size)
        