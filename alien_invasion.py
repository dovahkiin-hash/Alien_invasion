import sys

import pygame

from settings import settings
from spaceship import Spaceship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import gamestats
from button import button
from scoreboard import scoreboard
from game_screen import gamescreen
from music import Music_button


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.spaceship = Spaceship(self)
        self.game_screen = gamescreen(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.music = Music_button(self)
        self.create_fleet()
        self.settings.increase_speed()
        self.stats = gamestats(self)
        self.scoreboard = scoreboard(self)
        self.play_button = button(self, "play")
        self.clock = pygame.time.Clock()
        self.game_music = pygame.mixer.music.load('sounds/theme_song.mp3')
        pygame.mixer.music.play(-1)
        self.bullet_sound = pygame.mixer.Sound("sounds/GunShooting() (online-audio-converter.com).wav")
        self.alien_destroying = pygame.mixer.Sound('sounds/Explosion.wav')

    def spaceship_hit(self):
        if self.stats.spaceship_left > 0:
            self.stats.spaceship_left -= 1
            self.aliens.empty()
            self.scoreboard.prepare_spaceships()
            self.bullets.empty()
            self.create_fleet()
            self.spaceship.centre_spaceship()
            self.alien_destroying.play()
            pygame.mouse.set_visible(False)
            sleep(1)
        else:
            self.stats.game_active = False
            self.game_screen.draw_game_end_game_screen()
            pygame.display.flip()
            sleep(2)
            pygame.mouse.set_visible(True)

    def update_alien(self):
        self.check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.spaceship, self.aliens):
            self.spaceship_hit()
        self.check_alien_at_bottom()

    def check_alien_at_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.spaceship_hit()
                break

    def create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        spaceship_height = self.spaceship.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = self.settings.screen_height - (2 * alien_height) - spaceship_height
        number_rows = available_space_y // (2 * alien_height)
        number_aliens_x = available_space_x // (2 * alien_width)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def deleteing_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.spaceship.update()
                self.bullets.update()
                self.deleteing_bullets()
                self.update_alien()
            self.update_screen()

    def check_for_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.alien_destroying.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.stats.score += self.settings.alien_points
            self.scoreboard.prepare_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()
            self.scoreboard.stats.level += 1
            self.scoreboard.prepare_level()

    def check_play_button(self, mouse_position):
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked and not self.stats.game_active:
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.stats.game_active = True
            self.settings.initialize_dynamic_setting()
            self.stats.reset_stats()
            self.scoreboard.prepare_spaceships()
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.spaceship.centre_spaceship()
            pygame.mouse.set_visible(False)

    def check_sound_button(self, mouse_pos):
        if self.music.rect.collidepoint(mouse_pos):
            pygame.mixer.music.pause()

    def update_bullet(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        self.check_for_bullet_alien_collision()

    def update_screen(self):
        self.screen.blit(self.settings.image_background, [0, 0])
        self.spaceship.blirme()
        self.update_bullet()
        self.scoreboard.show_score()
        self.aliens.draw(self.screen)
        self.music.draw_sound_button()
        if not self.stats.game_active:
            self.game_screen.draw_game_Screen()
            self.play_button.draw_button()
            self.music.draw_sound_button()

        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self.check_play_button(mouse_position)
                self.check_sound_button(mouse_position)
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = True
        elif event.key == pygame.K_d:
            self.spaceship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = True
        elif event.key == pygame.K_a:
            self.spaceship.moving_left = True
        elif event.key == pygame.K_UP:
            self.spaceship.moving_up = True
        elif event.key == pygame.K_w:
            self.spaceship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.spaceship.moving_down = True
        elif event.key == pygame.K_s:
            self.spaceship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.bullet_sound.play()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = False
        elif event.key == pygame.K_d:
            self.spaceship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = False
        elif event.key == pygame.K_a:
            self.spaceship.moving_left = False

        elif event.key == pygame.K_UP:
            self.spaceship.moving_up = False
        elif event.key == pygame.K_w:
            self.spaceship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.spaceship.moving_down = False
        elif event.key == pygame.K_s:
            self.spaceship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
