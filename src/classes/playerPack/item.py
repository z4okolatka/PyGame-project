import pygame as pg
import main

class Item:
    @classmethod
    def init_game(cls, game):
        cls.game: main.Game = game
        cls.inventory = game.player.inventory

    def __init__(self, inventory, type_):
        self.inventory = inventory
        self.type = type_
        self.amount = 1

        try:
            self.image = pg.transform.scale(self.inventory.game.items_images[type_][0][0],
                                            (self.inventory.cell_size, self.inventory.cell_size))
        except KeyError:
            self.image = pg.Surface(
                (self.inventory.cell_size, self.inventory.cell_size))
            if self.type in self.inventory.game.accecory_types:
                self.image.fill('turquoise')
            else:
                self.image.fill('yellow')
        self.rect = self.image.get_rect()
