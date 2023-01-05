import pygame as pg
from src.classes import screenCamera
from src.classes import player
from src.classes import block
from src.classes import render
from src.classes import menu
from src.classes import infoDisplay
from src.classes import coordHelper
from src.classes import roomBarrier
from src.classes.utilites import *
from pathlib import Path
import src.setting as settings


class Game:
    def __init__(self):
        pg.init()

        self.FPS = settings.FPS
        self.clock = pg.time.Clock()

        # attributes
        self.deltatime = 1e-10
        self.paused = False

        # objects and object gorups
        self.camera = screenCamera.ScreenCamera(self)
        self.player = player.Player(self)
        self.barriers: dict[str: roomBarrier.Barrier] = {
            'left': roomBarrier.Barrier(
                (-self.camera.width, self.camera.centery), (5, self.camera.height * 3)),
            'right': roomBarrier.Barrier(
                (self.camera.width * 2, self.camera.centery), (5, self.camera.height * 3)),
            'top': roomBarrier.Barrier(
                (self.camera.width / 2, -self.camera.centery * 2), (self.camera.width * 3, 5)),
            'bottom': roomBarrier.Barrier(
                (self.camera.width / 2, self.camera.centery * 4), (self.camera.width * 3, 5))
        }
        self.collision_objects = [
            block.Block(
                (-self.camera.width, self.camera.centery), (5, self.camera.height * 3)),
            block.Block(
                (self.camera.width * 2, self.camera.centery), (5, self.camera.height * 3)),
            block.Block(
                (self.camera.width / 2, -self.camera.centery * 2), (self.camera.width * 3, 5)),
            block.Block(
                (self.camera.width / 2, self.camera.centery * 4), (self.camera.width * 3, 5))
        ]
        self.menu = menu.Menu(self, self.camera.display.get_size())
        self.render = render.Render(self)
        self.info = infoDisplay.InformationDisplay(self, pg.font.Font(
            Path(__file__).parent / "src/fonts/PressStart.ttf", 20))

    def run(self):
        self.running = True
        while self.running:
            # event handler
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = not self.paused
                if event.type == pg.MOUSEWHEEL:
                    if event.y > 0:
                        self.camera.scale = round(
                            clamp(0.5, self.camera._scale + .1, 2), 1)
                    else:
                        self.camera.scale = round(
                            clamp(0.5, self.camera._scale - .1, 2), 1)
                if event.type == pg.WINDOWMOVED:
                    self.paused = True

            # updating everything
            self.update()

            # drawing everything
            self.draw_game()
            self.info.draw(self.camera.display)
            if self.paused:
                self.draw_menu()

            # game loop
            pg.display.flip()
            self.deltatime = self.clock.tick(self.FPS) / 1000

        pg.quit()

    def update(self):
        if not self.paused:
            self.update_game()
        else:
            self.update_menu()

    def update_game(self):
        # temporary creating platforms
        for event in self.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = (self.camera.x + event.pos[0] / self.camera.scale,
                       self.camera.y + event.pos[1] / self.camera.scale)
                if event.button == 1:
                    self.collision_objects.append(
                        block.Block(pos, (200, 30)))
                if event.button == 3:
                    self.player.center = pos
        self.player.update()
        self.camera.follow_player()

    def update_menu(self):
        self.menu.update()

    def draw_game(self):
        self.camera.display.fill((50, 50, 50))
        self.render.draw_all()
        self.render.draw(self.barriers.values())

    def draw_menu(self):
        self.menu.draw(self.camera.display)


if __name__ == "__main__":
    game = Game()
    game.run()
