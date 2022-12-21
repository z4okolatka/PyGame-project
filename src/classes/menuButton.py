import pygame as pg
from pathlib import Path
pg.init()


class Button:
    def __init__(self, game, text, font=pg.font.Font(Path(__file__).parent.parent / "fonts/PressStart.ttf", 36), basecolor=(255, 255, 255), hovercolor=(150, 150, 150), size=(100, 50)):
        self.game = game
        self.text = text
        self.font = font
        self.bclr = basecolor
        self.hclr = hovercolor
        self.rendered = self.font.render(self.text, True, self.bclr)
        self.rect = self.rendered.get_rect()

    def update(self):
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False
        if self.hovered and pg.mouse.get_pressed()[0]:
            self._click_()

    def draw(self, surface, left, cy):
        if self.hovered:
            self.rendered = self.font.render(self.text, True, self.hclr)
        else:
            self.rendered = self.font.render(self.text, True, self.bclr)

        self.rect = self.rendered.get_rect()
        self.rect.left = left
        self.rect.centery = cy
        surface.blit(self.rendered, self.rect)
    
    def _click_(self):
        pass