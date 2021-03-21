import pygame


class gamescreen:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.Gamescreen = pygame.image.load('images/game_screen/game_screen1.png')
        self.rect1 = self.Gamescreen.get_rect()
        self.Game_end_screen = pygame.image.load('images/game_screen/game_over.png')
        self.rect2=self.Game_end_screen.get_rect()
        self.rect2 = self.Game_end_screen.get_rect()
        self.rect1 = self.Gamescreen.get_rect()

    def draw_game_Screen(self):
        self.screen.blit(self.Gamescreen, self.rect1)

    def draw_game_end_game_screen(self):
        self.screen.blit(self.Game_end_screen, self.rect2)
