import pygame


class settings:
    def __init__(self, ):
        # Don't change these settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.image_background = pygame.image.load('images/background/background_1.png')
        # you can change these settings
        self.bullet_speed = 12.5
        self.bullet_width =7
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 4
        self.spaceship_limit = 3
        self.speedup_scale = 1.2
        self.speedup_scale1 = 2.2
        self.fleet_drop_speed = 5
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.spaceship_speed = 10
        self.alien_speed = 5
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.spaceship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale1)
