import pygame as pg
from collections.abc import Iterable
from src.classes.utilites import *
import main


class Render():
    def __init__(self, game):
        self.game: main.Game = game
        self.display = self.game.camera.display

    def draw_all(self):
        self.draw(self.game.player)
        self.draw(self.game.collision_objects)
    
    def _draw_one_sprite(self, sprite):
        w, h = sprite.rect.size
        x, y = sprite.topleft

        scale = self.game.camera.scale

        # position
        x -= self.game.camera.x
        y -= self.game.camera.y

        # size
        x *= scale
        y *= scale

        # correcting position
        camWidth, camHeight = self.game.camera.display.get_size()
        x += camWidth * (1 - scale) / 2
        y += camHeight * (1 - scale) / 2        

        self.display.blit(scale_by(sprite.image, scale), (round(x), round(y), w, h))

    def draw(self, object_):
        if not isinstance(object_, Iterable):
            object_ = [object_]
        
        for sprite in object_:
            self._draw_one_sprite(sprite)
