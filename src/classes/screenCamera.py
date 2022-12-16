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

        # attributes
        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

    def follow_player(self):
        self.handle_x_offset()
        self.handle_y_offset()

    def handle_x_offset(self):
        pcx = self.game.player.centerx
        cx = self.offset_x + self.width / 2
        dx = pcx - cx

        self.offset_x += absmin(dx * 0.04,
                                self.game.player.max_vx * self.game.deltatime)

    def handle_y_offset(self):
        pcy = self.game.player.centery
        cy = self.offset_y + self.height / 2
        dy = pcy - cy

        self.offset_y += absmin(dy * 0.06,
                                self.game.player.max_vy * self.game.deltatime)
