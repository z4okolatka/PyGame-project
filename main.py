import pygame as pg
from src.classes.renderPack import screenCamera, render
from src.classes.playerPack import player, interface
from src.classes.mapPack import door, room, roomBarrier, block, trigger
from src.classes.menuPack import menu
from src.classes.utilsPack import infoDisplay
from src.classes.utilsPack.utilites import *
from pathlib import Path
import src.setting as settings


class Game:
    def __init__(self):
        pg.init()
        trigger.Trigger.init_game(self)

        self.FPS = settings.FPS
        self.clock = pg.time.Clock()

        # attributes
        self.deltatime = 1e-10
        self.paused = False
        self.list = []

        # objects and object gorups
        self.camera = screenCamera.ScreenCamera(self)
        self.player = player.Player(self)
        self.boundaries: dict[str: roomBarrier.Barrier] = {
            'left': roomBarrier.Barrier(
                (-self.camera.width, self.camera.centery), (5, self.camera.height * 3)),
            'right': roomBarrier.Barrier(
                (self.camera.width * 2, self.camera.centery), (5, self.camera.height * 3)),
            'top': roomBarrier.Barrier(
                (self.camera.width / 2, -self.camera.centery * 2), (self.camera.width * 3, 5)),
            'bottom': roomBarrier.Barrier(
                (self.camera.width / 2, self.camera.centery * 4), (self.camera.width * 3, 5))
        }
        self.menu = menu.Menu(self, self.camera.display.get_size())
        self.render = render.Render(self)
        self.ui = interface.UI(self)
        self.info = infoDisplay.InformationDisplay(self, pg.font.Font(
            Path(__file__).parent / "src/fonts/PressStart.ttf", 20))

        # starting room
        self.rooms = []
        self.rooms.append(room.Room(self, None, None, start_room=True))
        self.new_rooms_cords = [((-1, 1), (0, 3, 0, 0))]
        list(i for i in self.rooms[0].chunks if i.x == 0 and i.y == 1)[0].doors.append(door.Door((-100, 100), (20, 20), (-1, 1)))

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
                        self.camera.smooth_scale += .1
                    else:
                        self.camera.smooth_scale -= .1
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
            self.info.show('fps', self.clock.get_fps(), .01)

        pg.quit()

    def update(self):
        if not self.paused:
            self.update_game()
        else:
            self.update_menu()

    def update_game(self):
        # temporary creating platforms

        for event in self.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LSHIFT:
                    try:
                        self.list[0].destroy()
                        del self.list[0]
                    except:
                        pass
                    self.list.append(block.Block(
                        self.player.rect.midbottom, (100, 10), 'red'))
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = (self.camera.x + event.pos[0] / self.camera.scale,
                       self.camera.y + event.pos[1] / self.camera.scale)
                if event.button == 1:
                    block.Block(pos, (100, 10))
                if event.button == 3:
                    self.player.center = pos
        self.player.update()
        self.camera.follow_player()
        trigger.Trigger.activate_triggered()

    def update_menu(self):
        self.menu.update()

    def draw_game(self):
        self.camera.display.fill((50, 50, 50))
        self.render.draw_all()
        self.ui.draw_all()

    def draw_menu(self):
        self.menu.draw(self.camera.display)


if __name__ == "__main__":
    game = Game()
    game.run()
