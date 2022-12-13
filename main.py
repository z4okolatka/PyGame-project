import pygame as pg
from src.classes import screenCamera
from src.classes import player
import src.setting as settings


class Game:
    def __init__(self):
        pg.init()

        self.FPS = settings.FPS
        self.clock = pg.time.Clock()

        self.deltatime = 1e-10
        self.camera = screenCamera.screenCamera(self)
        self.player = player.Player(self)

    def run(self):
        running = True
        while running:
            # event handler
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # updating everything
            self.update()

            # drawing everything
            self.draw()

            # game loop
            pg.display.flip()
            self.deltatime = self.clock.tick(self.FPS) / 1000

        pg.quit()

    def update(self):
        self.player.update()

    def draw(self):
        self.camera.display.fill((50, 50, 50))

        self.player.draw(self.camera.display)


if __name__ == "__main__":
    game = Game()
    game.run()
