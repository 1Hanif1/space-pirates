import pygame
from pygame.sprite import Sprite


class EnemyShip(Sprite):
    def __init__(self, enemy_pos):
        super().__init__()
        self.image = pygame.image.load("./Assets/Images/alien_ship.png")
        self.image = pygame.transform.scale(
            self.image, (50, 50)
        )
        self.rect = self.image.get_rect()
        self.enemy_pos = enemy_pos
        self.rect.center = (enemy_pos.x, enemy_pos.y)

    def update(self):
        self.rect.center = (self.enemy_pos.x, self.enemy_pos.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
