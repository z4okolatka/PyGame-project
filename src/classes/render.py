import pygame as pg
import src.setting as settings
from src.classes import coordHelper
import main


class Render(coordHelper.FloatCords):
    def __init__(self, game):
        self.game: main.Game = game
        self.scale = self.game.camera.scale
        self.display = self.game.camera.display

    def update(self, objects: dict):
        self.player(objects['player'])
        self.collision_objects(objects['collision_objects'])

    def player(self, player):
        # middle_rect = player.rect.copy()
        # middle_rect.x = self.game.camera.display.get_width()//2
        # middle_rect.y = self.game.camera.display.get_height()//2
        # self.display.blit(player.image, middle_rect)
        self.draw(player)

    def collision_objects(self, collision_objects):
        for collision_object in collision_objects:
            self.draw(collision_object)

    def draw(self, object_):
        offset_rect = object_.rect.copy()
        offset_rect.x += self.game.camera.offset_x
        offset_rect.y += self.game.camera.offset_y

        self.display.blit(object_.image, offset_rect)
