import pygame
from variables import *


class Projectile:
    def __init__(self, x, y, screen):
        self.pos = pygame.Vector2(x, y)
        self.speed = PROJECTILE_SPEED

    def move(self, dt):
        self.pos.y -= self.speed * dt

    def check_collision(self, enemies):
        for enemy in enemies:
            # Adjust the radius as needed
            if self.pos.distance_to(enemy.pos) < (ENEMY_SIZE + 5):
                return enemy
        return None
