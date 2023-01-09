import pygame as pg
import random
from src.classes.renderPack import screenCamera, render
from src.classes.playerPack import player, interface, item
from src.classes.mapPack import door, room, roomBarrier, block, trigger, accessory, sword
from src.classes.menuPack import menu
from src.classes.utilsPack import infoDisplay
from src.classes.enemyPack import enemy, groundEnemy, airEnemy, turretEnemy
from src.classes.utilsPack import infoDisplay, keepRefs
from src.classes.utilsPack.utilites import *
from pathlib import Path
import src.setting as settings


class Game:
    def __init__(self):
        pg.init()
        keepRefs.KeepRefs.init_game(self)

        self.FPS = settings.FPS
        self.clock = pg.time.Clock()

        # attributes
        self.deltatime = 1e-10
        self.paused = False

        # objects and object gorups
        self.accecory_types = ['nimb', 'flash', 'truba', 'drill',
                               'banana', 'grib', 'air_forces']
        self.sword_types = ['wolfOdrill', 'niggaOshake', 'skibididaMdadaBOOM']
        self.list = []
        self.items = []
        self.camera = screenCamera.ScreenCamera(self)
        self.load_sprites()
        self.player = player.Player(self)
        item.Item.init_game(self)
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

        turretEnemy.TurretEnemy(self, (-100, 100))
        list(i for i in self.rooms[0].chunks if i.x == 0 and i.y == 1)[
            0].doors.append(door.Door((-100, 100), (20, 20), (-1, 1)))

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
                    sign = - event.y // abs(event.y)
                    inventory = self.player.inventory
                    ind = clamp(-1, inventory.selectedIndex +
                                sign, inventory.max_size)
                    if ind == -1:
                        ind = inventory.max_size - 1
                    elif ind == inventory.max_size:
                        ind = 0
                    inventory.selectedIndex = ind
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
            self.info.show(None, round(self.clock.get_fps()), .01)

        pg.quit()


    def load_sprites(self):
        self.items_images = {}
        sprite_path = Path.cwd() / 'src/sprites'
        
        for type_ in self.accecory_types:
            path = sprite_path / f'{type_}.png'
            image = pg.image.load(path).convert_alpha()
            self.items_images[type_] = image

    def update(self):
        if not self.paused:
            self.update_game()
        else:
            self.update_menu()

    def update_game(self):
        # temporary creating platforms
        self.key_pressed = pg.key.get_pressed()
        for event in self.events:
            event.pos = pg.mouse.get_pos()
            pos = (self.camera.x + event.pos[0] / self.camera.scale,
                   self.camera.y + event.pos[1] / self.camera.scale)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.items.append(
                        accessory.Accessory(
                            self, pos, random.choice(self.accecory_types))
                    )
                    sign = 1 if self.player.facing == 'right' else - 1
                    self.items[-1].vx = 1000 * sign
                    self.items[-1].vy = -1000
                if event.key == pg.K_2:
                    self.items.append(
                        sword.Sword(self, pos, random.choice(self.sword_types))
                    )
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
                if event.button == 3:
                    self.player.center = pos
        if self.key_pressed[pg.K_LSHIFT]:
            self.a = block.Block(
                (self.player.rect.centerx, self.player.rect.bottom + 5), (100, 10))
        else:
            self.a = None
        if self.key_pressed[pg.K_q]:
            self.camera.smooth_scale += self.camera.scale_step / 10
        if self.key_pressed[pg.K_e]:
            self.camera.smooth_scale -= self.camera.scale_step / 10

        self.player.update()
        self.camera.follow_player()
        [i.update() for i in enemy.Enemy.get_refs()]
        for i in self.items:
            i.update()
        trigger.Trigger.activate_allcls_triggered()
        self.info.show('hp',self.player.hp)

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
