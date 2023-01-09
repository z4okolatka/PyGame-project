import math

import pygame as pg
import src.setting as settings
from src.classes.utilsPack import coordHelper
from src.classes.playerPack import inventory
from src.classes.mapPack import collidableObject
from src.classes.utilsPack.utilites import *
from pathlib import Path
import main


class Enemy(pg.sprite.Sprite, coordHelper.FloatCords):
    __refs__ = []

    @classmethod
    def get_refs(cls):
        for obj in cls.__refs__:
            if obj is None:
                cls.__refs__.remove(obj)
                continue
            yield obj

    def destroy(self):
        Enemy.__refs__.remove(self)

    def __init__(self, game, cords=None):
        super().__init__()
        Enemy.__refs__.append(self)
        self.game: main.Game = game

        self.image: pg.Surface
        self.image = pg.image.load(Path.cwd() / 'src/sprites/kirill.png')
        self.image = pg.transform.scale(self.image, (90, 180))

        self._facing = 'right'
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

        # speed and position
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
        self.max_zoom_out = .2

        self.aggression_distance = 500
        self.damage = 5

    @property
    def distance_to_player(self):
        return math.sqrt((self.x - self.game.player.x) ** 2 + (self.y - self.game.player.y) ** 2)

    def movement(self):
        # self.horizontal_movement()
        # self.normalize_horizontal_speed()
        # self.move_x()
        # self.horizontal_collision()
        # self.rotate_image()
        #
        # self.vertical_movement()
        # self.normalize_vertical_speed()
        # self.move_y()
        # self.vertical_collision()
        pass

    def idle_movement(self):
        pass

    def update(self):
        if self.distance_to_player <= self.aggression_distance:
            self.movement()
        else:  # self.vy = 0
            self.idle_movement()

    def horizontal_movement(self):
        # if self.keydown(pg.K_d, keyboard) or self.keydown(pg.K_a, keyboard):
        #    self.vx = 0
        # if keyboard[pg.K_d]:
        #    self.vx += self.vx_acceleration
        # if keyboard[pg.K_a]:
        #    self.vx -= self.vx_acceleration
        # if not keyboard[pg.K_a] and not keyboard[pg.K_d] and self.vx:
        #    if self.vx < 0:
        #        self.vx += self.vx_acceleration
        #    else:
        #        self.vx -= self.vx_acceleration
        #    if abs(self.vx) <= self.vx_acceleration:
        #        self.vx = 0
        print(1)

    def normalize_horizontal_speed(self):
        if abs(self.vx) >= self.max_vx:
            self.vx /= abs(self.vx)
            self.vx *= self.max_vx

    def move_x(self):
        self.x += self.vx * self.game.deltatime
        self.rect.x = round(self.x)

    def rotate_image(self):
        if self.vx > 0:
            self.facing = 'right'
        elif self.vx < 0:
            self.facing = 'left'

    def horizontal_collision(self):
        for sprite in collidableObject.CollidableObject.get_collided(self):
            # climbing on small ledges
            if self.rect.bottom - sprite.rect.top <= 20 and abs(self.vy) <= 300:
                self.bottom = sprite.rect.top
            else:
                if self.rect.centerx <= sprite.rect.centerx and self.vx > 0:
                    self.right = sprite.rect.left
                    self.vx = 0
                elif self.rect.centerx > sprite.rect.centerx and self.vx < 0:
                    self.left = sprite.rect.right
                    self.vx = 0

        self.rect.x = round(self.x)

    def vertical_movement(self):
        # if self.keydown(pg.K_SPACE, keyboard) and self.jump_num:
        #    self.vy = -self.jump_initial_speed
        #    # self.jump_num -= 1
        # self.vy += self.gravity * self.game.deltatime
        print(2)

    def normalize_vertical_speed(self):
        if abs(self.vy) >= self.max_vy:
            self.vy /= abs(self.vy)
            self.vy *= self.max_vy

    def move_y(self):
        self.y += self.vy * self.game.deltatime
        self.vy += self.gravity * self.game.deltatime
        self.rect.y = round(self.y)

    def vertical_collision(self):
        for sprite in collidableObject.CollidableObject.get_collided(self):
            if self.rect.centery < sprite.rect.centery and self.vy > 0:
                self.vy = 0
                self.bottom = sprite.rect.top
                self.jump_num = self.max_jump_num
            elif self.rect.centery > sprite.rect.centery and self.vy < 0:
                self.vy = 0
                self.top = sprite.rect.bottom
        self.rect.y = round(self.y)

    def collision_with_player(self):
        if self.rect.colliderect(self.game.player.rect):
            self.collision_with_player_action()

    def collision_with_player_action(self):
        self.damage_player()

    def damage_player(self):
        if (pg.time.get_ticks() - self.game.player.damage_tick) / 1000 >= self.game.player.invulnerability_time:
            self.game.player.hp -= self.damage
            self.game.player.damage_tick = pg.time.get_ticks()

    def room_in(self):
        for room in self.game.rooms:
            for chunk in room.chunks:
                if self.rect.colliderect(chunk.chunk_area):
                    return room

    @property
    def facing(self):
        return self._facing

    @facing.setter
    def facing(self, direction):
        if self._facing == direction:
            return

        self._facing = direction
        self.image = pg.transform.flip(self.image, True, False)
