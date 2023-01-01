import pygame as pg
from src.classes.menuButton import Button
import main


class Menu:
    def __init__(self, game, size):
        self.game: main.Game = game

        self.bg = pg.Surface(size, pg.SRCALPHA)
        self.bg.fill((50, 50, 50, 100))
        self.rect = self.bg.get_rect()
        self.buttons: list[Button]
        self.buttons = [ResumeButton(self, 'Продолжить'), Button(
            self, 'Настройки'), QuitButton(self, 'Выйти')]
        self.len = len(self.buttons)
        self.buttonsHeight = sum(i.rect.height * 2 for i in self.buttons)

        self.selectedIndex = -1

    def update(self):
        for event in self.game.events:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_DOWN, pg.K_UP, pg.K_LEFT, pg.K_RIGHT):
                    self.on_press(event.key)
                if event.key == pg.K_RETURN:
                    button = self.buttons[self.selectedIndex]
                    button.on_click()
            if event.type == pg.MOUSEMOTION:
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(event.pos):
                        self.select(button)
                        break
                else:
                    self.clearSelection()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button = self.buttons[self.selectedIndex]
                    if button.rect.collidepoint(event.pos):
                        button.on_click()

    def on_press(self, key):
        if key in (pg.K_DOWN, pg.K_UP):
            self.handleVerticalArrow(key)
        else:
            pass

    def handleVerticalArrow(self, key):
        # up arrow
        if key == pg.K_UP:
            if not self.selectedIndex == 0:
                if self.selectedIndex == -1:
                    self.selectedIndex = self.len - 1
                else:
                    self.selectedIndex -= 1

        # down arrow
        if key == pg.K_DOWN:
            if not self.selectedIndex == self.len - 1:
                if self.selectedIndex == -1:
                    self.selectedIndex = 0
                else:
                    self.selectedIndex += 1

        self.select(self.buttons[self.selectedIndex])
        pg.mouse.set_pos(self.buttons[self.selectedIndex].rect.center)

    def clearSelection(self):
        self.selectedIndex = -1
        for i in self.buttons:
            i.selected = False

    def select(self, button):
        self.clearSelection()
        ind = self.buttons.index(button)
        self.buttons[ind].selected = True
        self.selectedIndex = ind

    def draw(self, surface: pg.Surface):
        for i, button in enumerate(self.buttons):
            button.draw(self.bg, 50, self.rect.h / 2 -
                        self.buttonsHeight / 2 + button.rect.height * 2 * i)
        surface.blit(self.bg, self.rect)


class ResumeButton(Button):
    def on_click(self):
        self.menu.game.paused = False


class QuitButton(Button):
    def on_click(self):
        self.menu.game.running = False
