from PIL import Image
import main
import pygame as pg


class Animation:
    def __init__(self, game, pack_name):
        self.game: main.Game = game
        self.images = self.game.items_images[pack_name]
        self.animationLen = len(self.images)

        self.animationFrameIndex = 0
        self.animTime = 0
        self.animated = True

        self.image = self.images[self.animationFrameIndex][0]

    @property
    def animationTime(self):
        return self.animTime

    @animationTime.setter
    def animationTime(self, n):
        self.animTime = n
        if self.animTime >= (dur := self.images[self.animationFrameIndex][1]):
            self.animTime -= dur
            self.animationFrameIndex = (self.animationFrameIndex + 1)\
                % self.animationLen
            self.image = self.images[self.animationFrameIndex][0]
