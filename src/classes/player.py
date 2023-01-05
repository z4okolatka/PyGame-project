import pygame as pg
import src.setting as settings
from src.classes import coordHelper
from src.classes import animation
from pathlib import Path
import main


class Player(pg.sprite.Sprite, coordHelper.FloatCords, animation.Animation):
    def __init__(self, game, cords=None):
        super().__init__()
        self.game: main.Game = game

        # image and rect
        animation.Animation.__init__(self, Path.cwd() / 'src/sprites/player.gif')
        self.image: pg.Surface
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

        self.max_vx = settings.PLAYER_MAX_HORIZONTAL_SPEED
        self.vx_acceleration = settings.PLAYER_HORIZONTAL_ACCELERATION

        self.max_vy = settings.PLAYER_MAX_VERTICAL_SPEED
        self.gravity = settings.PLAYER_FALL_ACCELERATION
        self.jump_initial_speed = settings.PLAYER_JUMP_INITIAL_SPEED
        self.max_jump_num = settings.PLAYER_MAX_JUMP_NUM
        self.jump_num = self.max_jump_num

        self._jump_height = 0

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

        # animation of sprite
        self.animationTime += self.game.deltatime * 1000

    def horizontal_movement(self, keyboard):
        if self.keydown(pg.K_d, keyboard) or self.keydown(pg.K_a, keyboard):
            self.vx = 0
        if keyboard[pg.K_d]:
            self.vx += self.vx_acceleration
        if keyboard[pg.K_a]:
            self.vx -= self.vx_acceleration
        if not keyboard[pg.K_a] and not keyboard[pg.K_d] and self.vx:
            if self.vx < 0:
                self.vx += self.vx_acceleration
            else:
                self.vx -= self.vx_acceleration
            if abs(self.vx) <= self.vx_acceleration:
                self.vx = 0

    def normalize_horizontal_speed(self):
        if abs(self.vx) >= self.max_vx:
            self.vx /= abs(self.vx)
            self.vx *= self.max_vx

    def move_x(self):
        self.x += self.vx * self.game.deltatime
        self.rect.x = round(self.x)

    def horizontal_collision(self):
        for sprite in self.game.collision_objects:
            if sprite.rect.colliderect(self.rect):
                # climbing on small ledges
                if self.rect.bottom - sprite.rect.top <= 20 and abs(self.vy) <= 300:
                    self.bottom = sprite.rect.top
                    break

                if self.rect.centerx <= sprite.rect.centerx and self.vx > 0:
                    self.right = sprite.rect.left
                    self.vx = 0
                elif self.rect.centerx > sprite.rect.centerx and self.vx < 0:
                    self.left = sprite.rect.right
                    self.vx = 0
                break

        self.rect.x = round(self.x)

    def vertical_movement(self, keyboard):
        if self.keydown(pg.K_SPACE, keyboard) and self.jump_num:
            self.vy = -self.jump_initial_speed
            self.jump_num -= 1
        self.vy += self.gravity * self.game.deltatime

    def normalize_vertical_speed(self):
        if abs(self.vy) >= self.max_vy:
            self.vy /= abs(self.vy)
            self.vy *= self.max_vy

    def move_y(self):
        self.y += self.vy * self.game.deltatime
        self.vy += self.gravity * self.game.deltatime
        self.rect.y = round(self.y)

    def vertical_collision(self):
        for sprite in self.game.collision_objects:
            if sprite.rect.colliderect(self.rect):
                if self.rect.centery < sprite.rect.centery and self.vy > 0:
                    self.vy = 0
                    self.bottom = sprite.rect.top
                    self.jump_num = self.max_jump_num
                elif self.rect.centery > sprite.rect.centery and self.vy < 0:
                    self.vy = 0
                    self.top = sprite.rect.bottom
                break

        self.rect.y = round(self.y)