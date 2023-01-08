import pygame as pg
from src.classes import coordHelper
import main


class Trigger(pg.sprite.Sprite, coordHelper.FloatCords):
    def __init__(self, game, centerpos, size):
        super().__init__()

        self.game: main.Game = game
        self.player = self.game.player

        self.image = pg.Surface(size)
        self.image.fill('red')
        self.rect = self.image.get_rect()

        self.rect.center = centerpos
        self.x = self.rect.x
        self.y = self.rect.y

    def collision_with_player(self):
        return self.player.rect.colliderect(self.rect)

    def update(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        if self.collision_with_player():
            self.action()
            if self in self.game.triggers:
                del self.game.triggers[self.game.triggers.index(self)]

    def action(self):
        pass
