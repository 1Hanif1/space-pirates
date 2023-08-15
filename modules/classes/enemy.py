import pygame
from modules.classes.projectile import Projectile
import random
from modules.classes.variables import *


class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed_x = ENEMY_SPEED_X
        self.speed_y = ENEMY_SPEED_Y
        self.projectile = None

    def move_forward_x(self, dt):
        self.pos.x += self.speed_x * dt

    def move_backward_x(self, dt):
        self.pos.x -= self.speed_x * dt

    def move_down_y(self, dt):
        self.pos.y += self.speed_y * dt

    def create_projectile(self):
        return Projectile(self.pos.x, self.pos.y)

    @staticmethod
    def shoot_projectiles(enemies, enemy_projectiles, enemy_last_shot_time, cooldown, screen, dt):
        current_time = pygame.time.get_ticks()
        if current_time - enemy_last_shot_time >= cooldown:
            random_enemy = random.choice(enemies)
            # Create Projectile
            enemy_projectile = random_enemy.create_projectile()
            # Add to `enemy_projectiles`
            enemy_projectiles.append(enemy_projectile)
            # Set timer to prevent spam
            enemy_last_shot_time = current_time

        # Loop through `enemy_projectiles` and move the projectiles
        for index, projectile in enumerate(enemy_projectiles):
            projectile.move_down(dt)
            if projectile.pos.y >= SCREEN_HEIGHT:
                del enemy_projectiles[index]
            pygame.draw.circle(
                screen,
                ENEMY_PROJECTILE_COLOR,
                (int(projectile.pos.x), int(projectile.pos.y)),
                PROJECTILE_SIZE
            )

        return enemy_last_shot_time
