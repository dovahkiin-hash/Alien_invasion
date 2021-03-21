import pygame.font
from spaceship import Spaceship


class scoreboard:
    def __init__(self, ai_game):
        self.image = pygame.image.load('images/spaceship/spaceship.png')
        self.rect = self.image.get_rect()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.bg_color = (0, 0, 0)

        self.text_color = (255, 225, 225)
        self.font = pygame.font.SysFont(None, 38)
        self.prepare_score()
        self.prepare_high_score()
        self.prepare_level()
        self.prepare_spaceships()

    def prepare_score(self):
        rounded_score = round(self.stats.score, -1)
        scoring_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(scoring_str, True, self.text_color, self.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prepare_high_score(self):
        high_score = round(self.stats.high_score, -2)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prepare_high_score()

    def prepare_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prepare_spaceships(self):
        self.spaceships = pygame.sprite.Group()
        for spaceship_number in range(self.stats.spaceship_left):
            spaceship = Spaceship(self.ai_game)
            spaceship.rect.x = 20 + spaceship_number * spaceship.rect.width
            spaceship.rect.y = 10
            self.rect.left = self.screen_rect.left
            self.spaceships.add(spaceship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.spaceships.draw(self.screen)
