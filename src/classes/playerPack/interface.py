import pygame as pg
from src.classes.utilsPack.utilites import *
import main


class UI:
    def __init__(self, game):
        self.game: main.Game = game
        self.rect = pg.Rect((0, 0), (self.game.camera.display.get_size()))

    def draw_all(self):
        self.draw(self.game.player.inventory)

    def draw(self, *args):
        if len(args) == 2:
            self.game.camera.display.blit(
                args[0], args[1]
            )
        else:
            self.game.camera.display.blit(
                args[0].image, args[0].rect
            )
