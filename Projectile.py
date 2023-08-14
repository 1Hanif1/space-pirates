import pygame
from variables import *


class Projectile:
    def __init__(self, x, y, screen):
        self.pos = pygame.Vector2(x, y)
        self.speed = PROJECTILE_SPEED

    def move(self, dt):
        self.pos.y -= self.speed * dt
