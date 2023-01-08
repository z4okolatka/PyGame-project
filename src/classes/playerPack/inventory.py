import pygame as pg
from collections import OrderedDict
from src.classes.utilsPack.coordHelper import FloatCords
import main

class DefaultOrderedDict(OrderedDict):
    def __init__(self, inventory, default_value):
        self.inventory: Inventory = inventory
        self.default_value = default_value

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.default_value

    def __setitem__(self, *args):
        return super().__setitem__(*args)


class Inventory(FloatCords):
    def __init__(self, game, max_size=10, cell_size=50, color=(0, 255, 0, 100)):
        super().__init__()

        self.game: main.Game = game
        self.max_size = max_size
        self.items = DefaultOrderedDict(self, 0)

        self.bg_clr = color
        self.image = pg.Surface(
            (max_size * (cell_size + 10), cell_size + 10), pg.SRCALPHA)
        self.image.fill(self.bg_clr)
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.game.camera.display.get_width() / 2, 0)

        self.x = self.rect.x
        self.y = self.rect.y
    
    def update(self):
        self.image.fill(self.bg_clr)
        self.image.blit()