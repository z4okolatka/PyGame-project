import pygame as pg
from collections import OrderedDict
from src.classes.coordHelper import FloatCords
import main


class Inventory(FloatCords):
    def __init__(self, game, max_size=10, cell_size=50):
        super().__init__()

        self.game: main.Game = game
        self.max_size = max_size
        self.items = OrderedDict()

        self.image = pg.Surface(
            (max_size * (cell_size + 10), cell_size + 10), pg.SRCALPHA)
        self.image.fill((0, 255, 0, 100))
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.game.camera.width / 2, 0)

        self.x = self.rect.x
        self.y = self.rect.y