import pygame as pg
import src.setting as settings
import main

class screenCamera:
    def __init__(self, game):
        self.game: main.Game = game

        # main surface
        self.display = pg.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    
    def fix_at(self, obj):
        """Fixing screen camera at some object so that camera follows it"""
        pass