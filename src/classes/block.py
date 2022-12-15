import pygame as pg

class Block(pg.sprite.Sprite):
    def __init__(self, centerpos, size):
        super().__init__()

        self.image = pg.Surface(size)
        self.image.fill('white')
        self.rect = self.image.get_rect()

        self.rect.center = centerpos