import pygame as pg
from src.classes import coordHelper
from collections.abc import Iterable
import main


class Render(coordHelper.FloatCords):
    def __init__(self, game):
        self.game: main.Game = game
        self.display = self.game.camera.display

    def draw_all(self):
        self.draw(self.game.player)
        self.draw(self.game.collision_objects)

    def draw(self, object_):
        if isinstance(object_, Iterable):
            for sprite in object_:
                offset_rect = sprite.rect.copy()
                offset_rect.x -= self.game.camera.offset_x
                offset_rect.y -= self.game.camera.offset_y

                self.display.blit(sprite.image, offset_rect)
        else:
            offset_rect = object_.rect.copy()
            offset_rect.x -= self.game.camera.offset_x
            offset_rect.y -= self.game.camera.offset_y

            self.display.blit(object_.image, offset_rect)
