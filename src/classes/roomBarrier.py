import pygame as pg
import src.classes.coordHelper as coordHelper

class Barrier(coordHelper.FloatCords):
    def __init__(self, center, size):
        super().__init__()

        self.image = pg.Surface(size)
        self.image.fill('red')
        self.rect = self.image.get_rect()

        # self.rect = pg.Rect((0, 0), size)
        
        self.rect.center = center

        self.x = self.rect.x
        self.y = self.rect.y