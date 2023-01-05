import pygame as pg
import screeninfo
import src.setting as settings
from src.classes.utilites import *
from src.classes.coordHelper import FloatCords
import main


class ScreenCamera(FloatCords):
    def __init__(self, game):
        self.game: main.Game = game

        # main surface
        if settings.FULL_SCREEN:
            monitor = screeninfo.get_monitors()[0]
            self.display = pg.display.set_mode(
                (monitor.width, monitor.height), pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode(
                (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.rect = self.display.get_rect()
        self.base_width = self.rect.width
        self.base_height = self.rect.height

        # attributes
        self.half_dw = 0
        self.half_dh = 0
        self._scale = 1
        self.x = 0
        self.y = 0

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, n):
        self.half_dw = (self.width - self.base_width * 1 / n)
        self.half_dh = (self.height - self.base_height * 1 / n)

        self.rect.width = self.base_width * (1 / n)
        self.rect.height = self.base_height * (1 / n)

        self.x += self.half_dw / 2
        self.y += self.half_dh / 2

        self._scale = n
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def follow_player(self):
        self.move_x()
        self.horizontal_collision()
        self.move_y()
        self.vertical_collision()

    def move_x(self):
        pcx = self.game.player.centerx
        self.dx = pcx - self.centerx

        if abs(self.dx) > 1:
            self.dx = self.dx * self.game.deltatime * 3.2
        self.x += self.dx
        self.rect.x = round(self.x)

    def horizontal_collision(self):
        barriers = self.game.barriers
        if self.left - 1 <= barriers['left'].right:
            self.left = barriers['left'].right
        if self.right + 1 >= barriers['right'].left:
            self.right = barriers['right'].left
        self.rect.x = round(self.x)

    def move_y(self):
        pcy = self.game.player.centery
        self.dy = pcy - self.centery

        self.y += self.dy * self.game.deltatime * 5.2
        self.rect.y = round(self.y)

    def vertical_collision(self):
        barriers = self.game.barriers
        if self.top - 1 <= barriers['top'].bottom:
            self.top = barriers['top'].bottom
        if self.bottom + 1 >= barriers['bottom'].top:
            self.bottom = barriers['bottom'].top
        self.rect.y = round(self.y)
