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


class GroundEnemy(enemy.Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.max_vx = 200

    def idle_movement(self):
        self.normalize_vertical_speed()
        self.move_y()
        self.vertical_collision()

    def movement(self):
        self.move_to_player_x()
        self.normalize_horizontal_speed()
        self.move_x()
        self.horizontal_collision()
        self.rotate_image()

        self.idle_movement()

    def move_to_player_x(self):
        if self.centerx - self.game.player.centerx < 0:
           self.vx += self.vx_acceleration
        else:
           self.vx -= self.vx_acceleration

