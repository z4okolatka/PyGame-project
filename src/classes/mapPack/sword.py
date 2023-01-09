import pygame as pg
from src.classes.playerPack.item import Item
from src.classes.renderPack.animation import Animation
from src.classes.mapPack.trigger import Trigger
from src.classes.mapPack.fallingObject import FallingObject
import main
from pathlib import Path


class SwordItem(Item):
    @classmethod
    def add(cls, type_):
        if cls.inventory.is_full() or type_ in cls.inventory.swords:
            return False
        cls.inventory.swords[type_] = SwordItem(cls.inventory, type_)
        return True


class SwordTriger(Trigger):
    def __init__(self, parent, centerpos, size):
        self.parent = parent
        super().__init__(centerpos, size, fill=False)

    def action(self):
        if SwordItem.add(self.parent.type):
            self.game.items.remove(self.parent)
            self.parent.trigger = None
    
    def follow(self):
        self.center = self.parent.center
        self.rect.topleft = round(self.x), round(self.y)


class Sword(FallingObject, Animation):
    def __init__(self, game, center, type_):
        FallingObject.__init__(self)
        self.game: main.Game = game
        self.type = type_
        self.animated = False

        self.image = pg.Surface((48, 96))
        self.image.fill('yellow')

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.trigger = SwordTriger(self, self.rect.center, self.rect.size)

        self.x, self.y = self.rect.topleft

    def update(self):
        super().update()

        self.trigger.follow()
        if self.animated:
            self.animationTime += self.game.deltatime * 1000
