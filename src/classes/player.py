import pygame as pg
import src.setting as settings
from src.classes import coordHelper
import main


class Player(pg.sprite.Sprite, coordHelper.FloatCords):
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

        self.max_vertical_speed = settings.PLAYER_MAX_VERTICAL_SPEED
        self.vertical_acceleration = settings.PLAYER_VERTICAL_ACCELERATION
        self.jump_speed = settings.PLAYER_JUMP_SPEED
        self.max_jump_num = settings.PLAYER_MAX_JUMP_NUM
        self.jump_num = self.max_jump_num

        # attributes
        self._lastKeyboard = pg.key.get_pressed()

    def keydown(self, key, pressed):
        """Returns true if key was just pressed"""
        return (not self._lastKeyboard[key]) and pressed[key]

    def update(self):
        # keyboard input
        kb = pg.key.get_pressed()

        self.horizontal_movement(kb)
        self.normalize_horizontal_speed()
        self.move_x()
        self.horizontal_collision()

        self.vertical_movement(kb)
        self.normalize_vertical_speed()
        self.move_y()
        self.vertical_collision()

        self._lastKeyboard = kb


    def horizontal_movement(self, keyboard):
        if self.keydown(pg.K_d, keyboard) or self.keydown(pg.K_a, keyboard):
            self.vx = 0
        if keyboard[pg.K_d]:
            self.vx += self.horizontal_acceleration * self.game.deltatime
        if keyboard[pg.K_a]:
            self.vx -= self.horizontal_acceleration * self.game.deltatime
        if not keyboard[pg.K_a] and not keyboard[pg.K_d] and self.vx:
            if self.vx < 0:
                self.vx += self.horizontal_acceleration * self.game.deltatime
            else:
                self.vx -= self.horizontal_acceleration * self.game.deltatime
            if abs(self.vx) < 1:
                self.vx = 0

    def normalize_horizontal_speed(self):
        if abs(self.vx) >= self.max_horizontal_speed * self.game.deltatime:
            self.vx /= abs(self.vx)
            self.vx *= self.max_horizontal_speed * self.game.deltatime

    def move_x(self):
        self.x += self.vx
        self.rect.x = round(self.x)

    def horizontal_collision(self):
        border_rect = self.rect.copy()

        for sprite in self.game.collision_objects:
            if sprite.rect.colliderect(border_rect):
                if border_rect.centerx <= sprite.rect.centerx and self.vx > 0:
                    self.right = sprite.rect.left
                    self.vx = 0
                    break
                elif border_rect.centerx > sprite.rect.centerx and self.vx < 0:
                    self.left = sprite.rect.right
                    self.vx = 0
                    break

        self.rect.x = round(self.x)

    def vertical_movement(self, keyboard):
        if self.keydown(pg.K_SPACE, keyboard) and self.jump_num:
            self.vy = self.jump_speed * -1
            self.jump_num -= 1
        self.vy += self.vertical_acceleration * self.game.deltatime

    def normalize_vertical_speed(self):
        if abs(self.vy) >= self.max_vertical_speed * self.game.deltatime:
            self.vy /= abs(self.vy)
            self.vy *= self.max_vertical_speed * self.game.deltatime

    def move_y(self):
        self.y += self.vy
        self.rect.y = round(self.y)

    def vertical_collision(self):
        border_rect = self.rect.copy()

        for sprite in self.game.collision_objects:
            if sprite.rect.colliderect(border_rect):
                if border_rect.bottom >= sprite.rect.top and abs(self.vy) > 0 and\
                        abs(border_rect.bottom - sprite.rect.top) < abs(border_rect.top - sprite.rect.bottom):
                    self.vy = 0
                    self.bottom = sprite.rect.top
                    self.jump_num = self.max_jump_num
                    break
                elif border_rect.top <= sprite.rect.bottom and abs(self.vy) > 0:
                    self.vy = 0
                    self.top = sprite.rect.bottom
                    break

        self.rect.y = round(self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
