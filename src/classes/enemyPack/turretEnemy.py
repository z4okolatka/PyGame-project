import math
import random

import pygame as pg
import src.setting as settings
from src.classes.utilsPack import coordHelper
from src.classes.playerPack import inventory
from src.classes.mapPack import collidableObject
from src.classes.utilsPack.utilites import *
from pathlib import Path
from src.classes.enemyPack import enemy, arrow
import pygame as pg
import main


class TurretEnemy(enemy.Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.max_vx = 700
        self.max_vy = 700
        self.speed = 500
        self.aggression_distance = 1000
        self.start_ticks = pg.time.get_ticks()
        self.cooldown = .5

    def idle_movement(self):
        self.normalize_vertical_speed()
        self.move_y()
        self.vertical_collision()

    def movement(self):
        self.rotate_to_player_x()
        self.normalize_horizontal_speed()
        self.move_x()
        self.horizontal_collision()
        self.rotate_image()
        self.idle_movement()
        self.shoot()

    def rotate_to_player_x(self):
        if self.centerx - self.game.player.centerx < 0:
            self.facing = 'right'
        else:
            self.facing = 'left'

    def shoot(self):
        if (pg.time.get_ticks() - self.start_ticks) / 1000 >= self.cooldown:
            angle = math.atan2(self.game.player.x - self.x,
                               self.game.player.y - self.y) + math.pi - math.pi * 3 / 2 + random.randint(-5, 5) / 100

            x = math.atan2(self.game.player.centerx - self.centerx,
                           self.game.player.centery - self.centery)

            if math.pi / 2 < x < math.pi:
                x -= math.pi / 2
            elif 0 < x < math.pi / 2:
                x += math.pi * 3 / 2
            elif -math.pi / 2 < x < 0:
                x += math.pi * 3 / 2
            elif -math.pi < x < -math.pi / 2:
                x += math.pi * 3 / 2

            angle = x
            print(math.degrees(x))
            # print(math.degrees(angle), self.x, self.y, self.game.player.x, self.game.player.y)
            vx, vy = 0, 0
            # if self.centerx - self.game.player.centerx < 0:
            vx = self.speed * math.cos(x)
            # elif int(self.centerx - self.game.player.centerx) == 0:
            #    vx = 0
            # else:
            #    vx -= self.max_vx * math.cos(angle)
            #
            # if self.centery - self.game.player.centery < 0:
            vy = self.speed * math.sin(x) * -1
            # else:
            #    vy -= self.max_vy * math.sin(angle + math.pi / 2)
            pg.draw.line(self.game.camera.display, pg.Color('red'), (self.centerx, self.centery),
                         (1000 * math.cos(x), 1000 * math.sin(x)))

            enemy.Enemy.__refs__.append(arrow.Arrow(self.game, (self.centerx, self.centery), vx, vy, x))
            self.start_ticks = pg.time.get_ticks()
