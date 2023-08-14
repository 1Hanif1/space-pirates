import pygame
from variables import *


class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed_x = ENEMY_SPEED_X
        self.speed_y = ENEMY_SPEED_Y

    def move_forward_x(self, dt):
        self.pos.x += self.speed_x * dt

    def move_backward_x(self, dt):
        self.pos.x -= self.speed_x * dt

    def move_down_y(self, dt):
        self.pos.y += self.speed_y * dt
