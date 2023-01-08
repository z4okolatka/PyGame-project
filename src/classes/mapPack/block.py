import pygame as pg
from src.classes.mapPack import collidableObject


class Block(pg.sprite.Sprite, collidableObject.CollidableObject):
    def __init__(self, centerpos, size):
        super().__init__()
        collidableObject.CollidableObject.__init__(self)

        self.image = pg.Surface(size)
        self.image.fill('white')
        self.rect = self.image.get_rect()

        self.rect.center = centerpos
        self.x = self.rect.x
        self.y = self.rect.y
    
    def update(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)