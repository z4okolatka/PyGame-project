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
        self.x = 0
        self.y = 0

    def follow_player(self):
        self.handle_x_offset()
        self.handle_y_offset()

    def handle_x_offset(self):
        pcx = self.game.player.centerx
        dx = pcx - self.centerx

        if abs(dx) > 1:
            dx = dx * self.game.deltatime * 3.2
        self.x += dx

    def handle_y_offset(self):
        pcy = self.game.player.centery
        cy = self.centery
        dy = pcy - cy

        self.y += dy * self.game.deltatime * 5.2
