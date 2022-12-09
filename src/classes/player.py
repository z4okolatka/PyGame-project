import pygame as pg
import src.setting as settings
import main


class Player(pg.sprite.Sprite):
    def __init__(self, game, cords=None):
        self.game: main.Game = game

        # surface
        self.image = pg.Surface((80, 160))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        # real coordinates
        if cords:
            self.rect.topleft = cords
        else:
            self.rect.topleft = ((
                settings.WINDOW_WIDTH // 2 - self.rect.width // 2,
                settings.WINDOW_HEIGHT // 2 - self.rect.height // 2
            ))
        self.x = self.rect.x
        self.y = self.rect.y

        # states
        self.vx = 0
        self.vy = 0
        self.jumping = False
        self.standingOnGround = False

    def update(self):
        # keyboard input
        keyboard = pg.key.get_pressed()
        if keyboard[pg.K_d]:
            self.vx = settings.PLAYER_SPEED_X * self.game.deltatime
        if keyboard[pg.K_a]:
            self.vx = -settings.PLAYER_SPEED_X * self.game.deltatime

        # stuff
        ...

        # updating position
        self.x += self.vx
        self.y += self.vy
        self.vx = 0

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
