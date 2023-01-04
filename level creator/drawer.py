import pygame as pg
from io import BytesIO
from PIL import Image
import threading


def minmax(min_, value, max_):
    return max(min_, min(value, max_))


class Drawer:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode((180, 180))

        self.data = []
        self.startpos = None
        self.endpos = None

    def get_rect(self):
        startpos = [minmax(0, self.startpos[0], self.screen.get_width()),
                    minmax(0, self.startpos[1], self.screen.get_height())]
        endpos = [minmax(0, self.endpos[0], self.screen.get_width()),
                  minmax(0, self.endpos[1], self.screen.get_height())]

        x = min(startpos[0], endpos[0])
        y = min(startpos[1], endpos[1])
        w = max(startpos[0], endpos[0]) - x
        h = max(startpos[1], endpos[1]) - y
        return pg.Rect(x, y, w, h)

    def run(self):
        self.running = True
        while self.running:
            # event handler
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.startpos = event.pos
                    if event.button == 3:
                        for i in self.data:
                            if i.collidepoint(event.pos):
                                self.data.remove(i)
                if event.type == pg.MOUSEMOTION:
                    self.endpos = event.pos
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.data.append(self.get_rect())
                        print(self.data[-1])
                        self.startpos = None
                        self.endpos = None
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_2:
                        self.hover_
            self.draw()

            pg.display.flip()

        image = BytesIO()
        pg.image.save(self.screen, image)
        pg.quit()

        thread = threading.Thread(target=Image.open(image).show)
        thread.start()

        return [list(i) for i in self.data], thread

    def draw(self):
        self.screen.fill((50, 50, 50))

        if self.startpos and self.endpos:

            pg.draw.rect(self.screen, 'white', self.get_rect())

        for rect in self.data:
            pg.draw.rect(self.screen, 'white', rect)
