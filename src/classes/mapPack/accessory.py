import pygame as pg
from src.classes.utilsPack import coordHelper
from src.classes.renderPack.animation import Animation
from src.classes.mapPack import trigger
import main
from pathlib import Path


class AccessoryTriger(trigger.Trigger):
    def __init__(self, parent, centerpos, size):
        self.parent = parent
        super().__init__(centerpos, size, fill=False)

    def action(self):
        self.game.items.remove(self.parent)
        self.player.inventory.items[self.parent.type] += 1
        self.parent.trigger = None


class Accessory(coordHelper.FloatCords, Animation):
    def __init__(self, game, midbottom, type_):
        self.game: main.Game = game
        self.type = type_

        match type_:
            case 'nimb':
                Animation.__init__(self, self.game, 'nimb')
                # self.image = pg.image.load(Path.cwd() / 'src/sprites/nimb.png')
            case _:
                self.image = pg.Surface((48, 48))
                self.image.fill('turquoise')
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom
        self.trigger = AccessoryTriger(self, self.rect.center, self.rect.size)

        self.x, self.y = self.rect.topleft
    
    def update(self):
        self.animationTime += self.game.deltatime * 1000
