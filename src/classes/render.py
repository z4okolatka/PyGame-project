import pygame as pg
from collections.abc import Iterable
from src.classes.objects import collidableObject, Trigger
from src.classes.utilites import *
import main


class Render():
    def __init__(self, game):
        self.game: main.Game = game
        self.display = self.game.camera.display

    def draw_all(self):
        self.draw(self.game.player)
        self.draw(collidableObject.get_refs())
        self.draw(Trigger.get_refs())
        self.draw(self.game.boundaries.values())

    def _draw_one_sprite(self, sprite):
        w, h = sprite.rect.size
        x, y = sprite.topleft

        # converting real coordinates into display coordinates
        x, y = self.handle_offset(x, y)
        x, y = self.handle_scale(x, y)

        self.display.blit(scale_by(sprite.image, self.game.camera.scale),
                          (round(x), round(y), w, h))

    def draw(self, object_):
        # check if object is sprite or sequence of sprites
        if not isinstance(object_, Iterable):
            object_ = (object_,)

        for sprite in object_:
            self._draw_one_sprite(sprite)

    def handle_offset(self, x, y):
        x -= self.game.camera.x
        y -= self.game.camera.y
        return x, y

    def handle_scale(self, x, y):
        x *= self.game.camera.scale
        y *= self.game.camera.scale
        return x, y
