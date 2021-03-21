import pygame

from pygame.sprite import Sprite
from game_stats import gamestats


class Alien(Sprite):
    def __init__(self, ai_game):
        super(Alien, self).__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = gamestats(self)

        if 1 <= self.stats.level <= 5:
            self.image = pygame.image.load('images/aliens/Alien_level_1.png')
        elif 6 <= self.stats.level <= 10:
            self.image = pygame.image.load('images/aliens/Alien_level_2.png')
        elif 11 <= self.stats.level <= 100:
            self.image = pygame.image.load('images/aliens/Alien_level_3.png')

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width

        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
