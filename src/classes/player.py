import pygame as pg
import src.setting as settings
import main


class Player(pg.sprite.Sprite):
    def __init__(self, game, cords=None):
        super().__init__()
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

        self.max_horizontal_speed = settings.PLAYER_MAX_HORIZONTAL_SPEED
        self.horizontal_acceleration = settings.PLAYER_HORIZONTAL_ACCELERATION

        # attributes
        self._lastKeyboard = pg.key.get_pressed()

    def keydown(self, key, pressed):
        """Returns true if key was just pressed"""
        return (not self._lastKeyboard[key]) and pressed[key]

    def update(self):
        self.horizontal_movement()
        self.normalize_horizontal_speed()
        self.rounding_cords()

    def horizontal_movement(self):
        # keyboard input
        keyboard = pg.key.get_pressed()

        if self.keydown(pg.K_d, keyboard) or self.keydown(pg.K_a, keyboard):
            self.vx = 0
        if keyboard[pg.K_d]:
            self.vx += self.horizontal_acceleration * self.max_horizontal_speed * self.game.deltatime
        if keyboard[pg.K_a]:
            self.vx -= self.horizontal_acceleration * self.max_horizontal_speed * self.game.deltatime
        if not keyboard[pg.K_a] and not keyboard[pg.K_d] and self.vx:
            if self.vx < 0:
                self.vx += self.horizontal_acceleration * self.max_horizontal_speed * self.game.deltatime
            else:
                self.vx -= self.horizontal_acceleration * self.max_horizontal_speed * self.game.deltatime
            if abs(self.vx) < 1:
                self.vx = 0
        self._lastKeyboard = keyboard

    def normalize_horizontal_speed(self):
        if abs(self.vx) >= self.max_horizontal_speed * self.game.deltatime:
            self.vx /= abs(self.vx)
            self.vx *= self.max_horizontal_speed * self.game.deltatime
        self.x += self.vx

    def rounding_cords(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
