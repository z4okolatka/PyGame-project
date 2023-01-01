import pygame as pg
import main

pg.init()

class Data:
    def __init__(self, game, key, value, deltatime):
        self.game = game
        self.key = key
        self.value = value
        self.next = value
        self.time = 0
        self.dt = deltatime
    
    def getV(self):
        self.time += self.game.deltatime
        if self.time >= self.dt:
            self.time = 0
            value = self.value
            self.value = self.next
            return f'{self.key} = {value}'
        return f'{self.key} = {self.value}'

    
    def setV(self, value):
        self.next = value

class InformationDisplay:
    def __init__(self, game, font):
        self.game: main.Game = game

        self.rows = {}
        self.font: pg.font.Font = font
        self.deltatime = 0
        self.drawTime = 1
    
    def show(self, key, value, dt = .1):
        if key in self.rows:
            self.rows[key].setV(value)
        else:
            self.rows[key] = Data(self.game, key, value, dt)

    def draw(self, surface):
        self.deltatime += self.game.deltatime
        for i, data in enumerate(self.rows.values()):
            row = data.getV()
            surf = self.font.render(row, True, 'white')
            rect = surf.get_rect()
            to_draw = pg.Surface(rect.size, pg.SRCALPHA)
            to_draw.fill((0, 0, 0, 0))
            to_draw.blit(surf, rect)
            rect = to_draw.get_rect()
            rect.top = i * rect.height + 10
            rect.left = 10
            surface.blit(to_draw, rect)
        
        if not self.deltatime < self.drawTime:
            self.rows.clear()
            self.deltatime = 0