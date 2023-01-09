import pygame as pg
from src.classes.utilsPack import coordHelper, keepRefs
import main


class Trigger(pg.sprite.Sprite, coordHelper.FloatCords, keepRefs.KeepRefs):
    @classmethod
    def get_allcls_triggered(cls):
        for inst in cls.get_allcls_refs():
            if inst.is_triggering():
                yield inst

    @classmethod
    def activate_allcls_triggered(cls):
        for trigger in cls.get_allcls_triggered():
            trigger.activate()

    def __init__(self, centerpos, size, fill=False):
        super().__init__()
        keepRefs.KeepRefs.__init__(self)

        self.game = self.__class__.game
        self.player = self.game.player

        if fill:
            self.image = pg.Surface(size)
            self.image.fill('red')
        else:
            self.image = pg.Surface(size, pg.SRCALPHA)
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
