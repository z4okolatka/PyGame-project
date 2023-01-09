import math

import pygame as pg
import src.setting as settings
from src.classes.utilsPack import coordHelper
from src.classes.playerPack import inventory
from src.classes.mapPack import collidableObject
from src.classes.utilsPack.utilites import *
from pathlib import Path
from src.classes.enemyPack import enemy
import main


class Arrow(enemy.Enemy):
    def __init__(self, game, pos, vx, vy, angle):

        super().__init__(game, pos)
        self.max_vx = 200
        self.max_vy = 200
        self.vx = vx
        self.vy = vy
        self.aggression_distance = 10 ** 10
        self.image = pg.image.load(Path.cwd() / 'src/sprites/drill.png')
        self.image = pg.transform.scale(self.image, (64, 64))

        def rotate(img, pos, angle):
            w, h = img.get_size()
            img2 = pg.Surface((w * 2, h * 2), pg.SRCALPHA)
            img2.blit(img, (w - pos[0], h - pos[1]))
            return pg.transform.rotate(img2, angle)

        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, math.degrees(angle) - 90)

        # self.x = self.rect.x
        # self.y = self.rect.y

    def idle_movement(self):
        pass

    def move_y(self):
        self.y += self.vy * self.game.deltatime
        self.rect.y = round(self.y)

    def movement(self):
        # self.normalize_horizontal_speed()
        self.move_x()
        # self.horizontal_collision()
        # self.normalize_vertical_speed()
        self.move_y()
        # self.vertical_collision()
        self.collision_with_player()
        self.walls_collision()

        self.idle_movement()

    def walls_collision(self):
        try:
            for refs in collidableObject.CollidableObject.get_refs():
                # print(refs.rect)
                if self.rect.colliderect(refs.rect):
                    self.destroy()
        except:
            pass

    def collision_with_player_action(self):
        self.damage_player()
        self.destroy()
