import pygame


class Music_button:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.music_image = pygame.image.load('images/sound.png')
        self.rect = self.music_image.get_rect()
        self.rect.bottom = self.screen_rect.bottom

    def draw_sound_button(self):
        self.screen.blit(self.music_image, self.rect)
