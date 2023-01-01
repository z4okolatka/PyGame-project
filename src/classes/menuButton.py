import pygame as pg
from pathlib import Path
import src.classes.menu as Menu


pg.init()


class Button:
    def __init__(self, menu, text, font=pg.font.Font(Path(__file__).parent.parent / "fonts/PressStart.ttf", 36), basecolor=(255, 255, 255), hovercolor=(150, 150, 150), size=(100, 50)):
        self.menu: Menu.Menu = menu

        self.text = text
        self.font = font
        self.bclr = basecolor
        self.hclr = hovercolor
        self.rendered = self.font.render(self.text, True, self.bclr)
        self.rect = self.rendered.get_rect()

        self.selected = False

    def draw(self, surface, left, cy):
        if self.selected:
            self.rendered = self.font.render(self.text, True, self.hclr)
        else:
            self.rendered = self.font.render(self.text, True, self.bclr)

        self.rect = self.rendered.get_rect()
        self.rect.left = left
        self.rect.centery = cy
        surface.blit(self.rendered, self.rect)

    def on_click(self):
        pass
