import pygame as pg
import src.setting as settings
import main
import math


class Player(pg.sprite.Sprite):
    def __init__(self, game, cords=None):
        self.game: main.Game = game

        # surface
        self.image = pg.Surface((80, 160))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        # float coordinates
        if cords:
            self.rect.topleft = cords
        else:
            display = self.game.camera.display
            self.rect.topleft = ((
                display.get_width() // 2 - self.rect.width // 2,
                display.get_height() // 2 - self.rect.height // 2
            ))

        self.x = self.rect.x
        self.y = self.rect.y
        self.vx = 0
        self.vy = 0

        # attributes
        self._lastKeyboard = pg.key.get_pressed()

    def keydown(self, key, pressed):
        """Returns true if key was just pressed"""
        return (not self._lastKeyboard[key]) and pressed[key]

    def update(self):
        # keyboard input
        keyboard = pg.key.get_pressed()

        # horizontal movement
        if self.keydown(pg.K_d, keyboard) or self.keydown(pg.K_a, keyboard):
            self.vx = 0
        if keyboard[pg.K_d]:
            self.vx += 30 * self.game.deltatime
        if keyboard[pg.K_a]:
            self.vx -= 30 * self.game.deltatime
        if not keyboard[pg.K_a] and not keyboard[pg.K_d] and self.vx:
            self.vx *= .92  # friction coefficient
            if abs(self.vx) < 1:
                self.vx = 0

        # normalize horizontal speed
        if abs(self.vx) >= settings.MAX_HORIZONTAL_SPEED * self.game.deltatime:
            self.vx /= abs(self.vx)
            self.vx *= settings.MAX_HORIZONTAL_SPEED * self.game.deltatime
        self.x += self.vx

        # flooring cords
        self.rect.x = math.floor(self.x)
        self.rect.y = math.floor(self.y)

        self._lastKeyboard = keyboard

    def draw(self, surface):
        surface.blit(self.image, self.rect)
