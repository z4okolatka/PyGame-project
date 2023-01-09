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


class AirEnemy(enemy.Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.max_vx = 400
        self.max_vy = 400
        self.aggression_distance = 1000

    def idle_movement(self):
        self.normalize_vertical_speed()
        self.move_y()
        self.vertical_collision()

    def move_y(self):
        self.y += self.vy * self.game.deltatime
        self.rect.y = round(self.y)

    def movement(self):
        self.move_to_player_xy()
        self.normalize_horizontal_speed()
        self.move_x()
        self.horizontal_collision()
        self.rotate_image()
        self.idle_movement()
        self.vy = 0
        self.idle_movement()

    def move_to_player_xy(self):
        angle = math.atan(abs(self.game.player.x - self.x) / abs(self.game.player.y - self.y + 0.00001))

        if self.centerx - self.game.player.centerx < 0:
            self.vx += self.max_vx * math.cos(angle)
        elif int(self.centerx - self.game.player.centerx) == 0:
            self.vx = 0
        else:
            self.vx -= self.max_vx * math.cos(angle)

        if self.centery - self.game.player.centery < 0:
            self.vy += self.max_vy * math.sin(angle + math.pi/2)
        else:
            self.vy -= self.max_vy * math.sin(angle + math.pi/2)

       # print('/n',self.vx,self.vy, math.degrees(angle))
