import pygame
from pygame.sprite import Sprite
from modules.classes.variables import PROJECTILE_SPEED, ENEMY_SIZE


class Projectile:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed = PROJECTILE_SPEED

    def move_up(self, dt):
        self.pos.y -= self.speed * dt

    def move_down(self, dt):
        self.pos.y += self.speed * dt

    def check_collision(self, enemies):
        for enemy in enemies:
            # Adjust the radius as needed
            if self.pos.distance_to(enemy.pos) < (ENEMY_SIZE + 5):
                return enemy
        return None
