import pygame as pg
import screeninfo
import src.setting as settings
import main


class ScreenCamera:
    def __init__(self, game):
        self.game: main.Game = game


        # main surface
        if settings.FULL_SCREEN:
            monitor = screeninfo.get_monitors()[0]
            self.display = pg.display.set_mode((monitor.width, monitor.height), pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    def fix_at(self, obj):
        """Fixing screen camera at some object so that camera follows it"""
        pass
