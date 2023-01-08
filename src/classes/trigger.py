import pygame as pg
from src.classes import coordHelper
import main


class Trigger(pg.sprite.Sprite, coordHelper.FloatCords):
    __refs__ = []

    @classmethod
    def get_refs(cls):
        return cls.__refs__

    @classmethod
    def get_triggered(cls):
        return list(trigger for trigger in cls.__refs__ if trigger.is_triggering())
    
    @classmethod
    def activate_triggered(cls):
        for trigger in cls.get_triggered():
            trigger.activate()

    def __init__(self, game, centerpos, size):
        super().__init__()
        Trigger.__refs__.append(self)

        self.game: main.Game = game
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
        try:
            Trigger.__refs__.remove(self)
        except:
            pass
    
    def destroy(self):
        Trigger.__refs__.remove(self)

    def action(self):
        pass
