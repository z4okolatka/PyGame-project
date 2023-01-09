import pygame as pg
from collections import OrderedDict
from src.classes.utilsPack.coordHelper import FloatCords
from pathlib import Path
import main


class DefaultOrderedDict(OrderedDict):
    def __init__(self, *args, inventory=None, default_value=None):
        super().__init__(*args)
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
    def __init__(self, game, max_size=10, cell_size=50, color=(200, 200, 200, 50)):
        super().__init__()
        self.game: main.Game = game

        self.max_size = max_size
        self.cell_size = cell_size
        self.accessories = DefaultOrderedDict(inventory=self, default_value=0)
        self.swords = DefaultOrderedDict(inventory=self, default_value=0)
        self.selectedIndex = 0

        self.bg_clr = color
        self.font = pg.font.Font(
            Path.cwd() / "src/fonts/PressStart.ttf", 10)
        self.image = pg.Surface(
            (max_size * (cell_size + 10), cell_size + 10), pg.SRCALPHA)
        self.image.fill(self.bg_clr)
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.game.camera.display.get_width() / 2, 0)

        self.x = self.rect.x
        self.y = self.rect.y

    def is_full(self):
        return len(self.accessories) + len(self.swords) == self.max_size

    def update(self):
        self.game.info.show('index', self.selectedIndex)
        self.image.fill(self.bg_clr)
        items = DefaultOrderedDict(self.swords | self.accessories)
        for x, item in enumerate(items.values()):
            rect = item.rect
            rect.x = 5 + (self.cell_size + 10) * x
            rect.y = 5
            text = self.font.render(str(item.amount), True, 'white')
            text_rect = text.get_rect()
            text_rect.topright = rect.topright
            self.image.blit(item.image, rect)
            self.image.blit(text, text_rect)
        pg.draw.rect(self.image, 'white', pg.Rect((5 + self.selectedIndex *( self.cell_size + 10)), 5, self.cell_size, self.cell_size), 3)