import pygame as pg
from src.classes.utilsPack import coordHelper
import weakref
import main


class Trigger(pg.sprite.Sprite, coordHelper.FloatCords):
    __refs__ = []

    @classmethod
    def init_game(cls, game):
        cls.game = game

    @classmethod
    def get_refs(cls):
        for obj in cls.__refs__:
            inst_obj = obj()
            if inst_obj is None:
                cls.__refs__.remove(obj)
                continue
            yield inst_obj

    @classmethod
    def get_triggered(cls):
        for obj in cls.__refs__:
            inst_obj = obj()
            if inst_obj is None:
                cls.__refs__.remove(obj)
                continue
            if inst_obj.is_triggering():
                yield inst_obj
    
    @classmethod
    def activate_triggered(cls):
        for trigger in cls.get_triggered():
            trigger.activate()

    def __init__(self, centerpos, size):
        super().__init__()
        Trigger.__refs__.append(weakref.ref(self))

        self.game = Trigger.game
        self.player = self.game.player

        self.image = pg.Surface(size)
        self.image.fill('red')
        self.rect = self.image.get_rect()

        self.rect.center = centerpos
        self.x = self.rect.x
        self.y = self.rect.y

    def is_triggering(self):
        return self.rect.colliderect(self.player)

    def activate(self):
        self.action()

    def action(self):
        pass
