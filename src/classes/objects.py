import pygame as pg
from src.classes.coordHelper import FloatCords
import main


class collidableObject(FloatCords):
    __refs__ = []

    @classmethod
    def get_refs(cls):
        return cls.__refs__

    @classmethod
    def check_all_collisions(cls, sprite):
        return list(object_ for object_ in cls.__refs__ if object_.colliding(sprite))

    def colliding(self, sprite):
        return self.rect.colliderect(sprite)

    def __init__(self):
        super().__init__()
        collidableObject.__refs__.append(self)

    def destroy(self):
        self.collidableObject.__refs__.remove(self)


class Trigger(pg.sprite.Sprite, FloatCords):
    __refs__ = []

    def __init__(self, game, centerpos, size):
        super().__init__()
        Trigger.__refs__.append(self)

        self.game: main.Game = game
        self.player = self.game.player

        self.image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.circle(self.image, 'red', (size[0] / 2, size[1] / 2), size[0] / 2)
        self.rect = self.image.get_rect()

        self.rect.center = centerpos
        self.x = self.rect.x
        self.y = self.rect.y

    @classmethod
    def get_refs(cls):
        return cls.__refs__

    @classmethod
    def get_triggered(cls):
        return list(object_ for object_ in cls.__refs__ if object_.collision_with_player())

    def collision_with_player(self):
        return self.rect.colliderect(self.player.rect)

    def update(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        if self.collision_with_player():
            self.action()
            if self in self.game.triggers:
                del self.game.triggers[self.game.triggers.index(self)]

    def action(self):
        pass

class Ring(Trigger):
    def __init__(self, game, centerpos):
        super().__init__(game, centerpos, (50, 50))

        self.image = pg.Surface((40, 20))
        self.image.fill('turquoise')
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.topleft
        
        