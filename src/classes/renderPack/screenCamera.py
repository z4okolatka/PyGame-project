import pygame as pg
import screeninfo
import src.setting as settings
from math import ceil
from src.classes.utilsPack.utilites import *
from src.classes.utilsPack.coordHelper import FloatCords
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
        self.image = pg.Surface(self.display.get_size(), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.base_width = self.rect.width
        self.base_height = self.rect.height

        # attributes
        self.half_dw = 0
        self.half_dh = 0
        self._scale = 1
        self.scale_step = 0.1
        self.smooth_scale = 0
        self.prevent_scale = [0, 0]
        self.prevent_zoom_out = [False, False]
        self.x = 0
        self.y = 0

        pg.draw.line(self.image, 'blue', (self.width / 2, 0),
                     (self.width / 2, self.height), 2)
        pg.draw.line(self.display, 'blue', (0, self.height / 2),
                     (self.width, self.height / 2), 2)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, n):
        if any(self.prevent_zoom_out) and n < self.scale:
            return
        
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
        self.smooth_zoom()
        self.move_x()
        self.horizontal_collision()
        self.move_y()
        self.vertical_collision()

    def smooth_zoom(self):
        if not self.smooth_scale:
            return
        sign = self.smooth_scale / abs(self.smooth_scale)
        self.scale += sign * 0.001
        self._scale = round(
            clamp(self.game.player.max_zoom_out, self._scale, 2), 3)
        self.smooth_scale -= sign * 0.001
        self.smooth_scale = round(self.smooth_scale, 3)

    def move_x(self):
        pcx = self.game.player.centerx
        self.dx = pcx - self.centerx

        if abs(self.dx) > 1:
            self.dx = self.dx * self.game.deltatime * 3.2
        self.x += self.dx
        self.rect.x = round(self.x)

    def horizontal_collision(self):
        # prevent camera move outside left and right boundaries
        try:
            boundaries = self.game.player.room_in().boundaries
        except:
            return
        overlap = self.width / 10
        # width = boundaries['right'].left - boundaries['left'].right

        if self.left - 1 + overlap <= boundaries['left'].right:
            self.left = boundaries['left'].right - overlap
        if self.right + 1 - overlap >= boundaries['right'].left:
            self.right = boundaries['right'].left + overlap
        self.rect.x = round(self.x)

    def move_y(self):
        pcy = self.game.player.centery
        self.dy = pcy - self.centery

        self.y += self.dy * self.game.deltatime * 5.2
        self.rect.y = round(self.y)

    def vertical_collision(self):
        # prevent camera move outside top and bottom boundaries
        try:
            boundaries = self.game.player.room_in().boundaries
        except:
            return
        overlap = self.height / 10
        # height = boundaries['bottom'].top - boundaries['top'].bottom

        if self.top - 1 + overlap <= boundaries['top'].bottom:
            self.top = boundaries['top'].bottom - overlap
        if self.bottom + 1 - overlap >= boundaries['bottom'].top:
            self.bottom = boundaries['bottom'].top + overlap
        self.rect.y = round(self.y)