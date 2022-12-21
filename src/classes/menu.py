import pygame as pg
from src.classes.menuButton import Button

class Menu:
    def __init__(self, game, size):
        self.game = game

        self.bg = pg.Surface(size, pg.SRCALPHA)
        self.bg.fill((50, 50, 50, 100))
        self.rect = self.bg.get_rect()
        self.buttons = [ResumeButton(game, 'Продолжить'), Button(game, 'Настройки'), QuitButton(game, 'Выйти')]
        self.buttonsHeight = sum(i.rect.height * 2 for i in self.buttons)
    
    def update(self):
        for i in self.buttons:
            i.update()

    def draw(self, surface):
        for i, button in enumerate(self.buttons):
            button.draw(self.bg, 50, self.rect.h / 2 - self.buttonsHeight / 2 + button.rect.height * 2 * i)
        surface.blit(self.bg, self.rect)

class ResumeButton(Button):
    def _click_(self):
        self.game.paused = False


class QuitButton(Button):
    def _click_(self):
        self.game.running = False