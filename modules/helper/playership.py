import pygame
from pygame.sprite import Sprite


class PlayerShip(Sprite):
    def __init__(self, player_pos):
        super().__init__()
        self.image = pygame.image.load("./Assets/Images/jet.png")
        self.image = pygame.transform.scale(
            self.image, (70, 70)
        )
        self.rect = self.image.get_rect()
        self.player_pos = player_pos
        self.rect.center = (player_pos.x, player_pos.y)

    def update(self):
        self.rect.center = (self.player_pos.x, self.player_pos.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
