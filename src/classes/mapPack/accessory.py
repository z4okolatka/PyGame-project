import pygame as pg
from src.classes.playerPack.item import Item
from src.classes.renderPack.animation import Animation
from src.classes.mapPack.trigger import Trigger
from src.classes.mapPack.fallingObject import FallingObject
import main
from pathlib import Path


class AccessoryItem(Item):
    @classmethod
    def add(cls, type_):
        if cls.inventory.is_full():
            if type_ not in cls.inventory.accessories:
                return False
            cls.inventory.accessories[type_].amount += 1
            return True
        if type_ not in cls.inventory.accessories:
            cls.inventory.accessories[type_] = AccessoryItem(
                cls.inventory, type_)
        else:
            cls.inventory.accessories[type_].amount += 1
        return True


class AccessoryTriger(Trigger):
    def __init__(self, parent, centerpos, size):
        self.parent = parent
        super().__init__(centerpos, size, fill=False)

    def action(self):
        if AccessoryItem.add(self.parent.type):
            self.game.items.remove(self.parent)
            self.parent.trigger = None
    
    def follow(self):
        self.center = self.parent.center
        self.rect.topleft = round(self.x), round(self.y)


class Accessory(Animation, FallingObject):
    def __init__(self, game, center, type_):
        FallingObject.__init__(self)
        self.game: main.Game = game
        self.type = type_
        self.animated = False

        if type_ in self.game.accecory_types:
            self.image = self.game.items_images[type_]
        else:
            self.image = pg.Surface((48, 48))
            self.image.fill('turquoise')

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.trigger = AccessoryTriger(self, self.rect.center, self.rect.size)

        self.x, self.y = self.rect.topleft

    def update(self):
        super().update()

        self.trigger.follow()
        if self.animated:
            self.animationTime += self.game.deltatime * 1000