import pygame as pg
from src.classes import screenCamera
from src.classes import player
from src.classes import block
import src.setting as settings


class Game:
    def __init__(self):
        pg.init()

        self.FPS = settings.FPS
        self.clock = pg.time.Clock()

        self.deltatime = 1e-10
        self.camera = screenCamera.ScreenCamera(self)
        self.player = player.Player(self)
        self.collision_objects = pg.sprite.Group()
        self.collision_objects.add([
            block.Block((5, self.camera.display.get_height() / 2),
                        (10, self.camera.display.get_height())),
            block.Block((self.camera.display.get_width(
            ) - 5, self.camera.display.get_height() / 2), (10, self.camera.display.get_height())),
            block.Block((self.camera.display.get_width() // 2, self.camera.display.get_height() - 5),
                        (self.camera.display.get_width(), 10)),
            block.Block((self.camera.display.get_width() - 200, 400),
                        (400, 100)),
            block.Block((200, 400),
                        (400, 100)),
            block.Block((self.camera.display.get_width() // 2, 650),
                        (300, 100)),
        ])

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
        self.collision_objects.draw(self.camera.display)


if __name__ == "__main__":
    game = Game()
    game.run()
