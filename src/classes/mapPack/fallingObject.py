from src.classes.utilsPack import coordHelper
from src.classes.mapPack import collidableObject
import src.setting as settings


class FallingObject(coordHelper.FloatCords):
    def __init__(self):
        self.vx = 0
        self.vy = 0
        self.max_vy = settings.PLAYER_MAX_VERTICAL_SPEED
        self.gravity = settings.PLAYER_FALL_ACCELERATION

    def update(self):
        self.horizontal_movement()
        self.move_x()
        self.horizontal_collision()

        self.vertical_movement()
        self.normalize_vertical_speed()
        self.move_y()
        self.vertical_collision()

    def horizontal_movement(self):
        self.vx *= 0.96
        if abs(self.vx) <= 10:
            self.vx = 0

    def vertical_movement(self):
        self.vy += self.gravity * self.game.deltatime

    def move_x(self):
        self.x += self.vx * self.game.deltatime
        self.rect.x = round(self.x)

    def horizontal_collision(self):
        for sprite in collidableObject.CollidableObject.get_collided(self):
            if self.rect.centerx <= sprite.rect.centerx and self.vx > 0:
                self.right = sprite.rect.left
                self.vx = 0
            elif self.rect.centerx > sprite.rect.centerx and self.vx < 0:
                self.left = sprite.rect.right
                self.vx = 0

        self.rect.x = round(self.x)

    def normalize_vertical_speed(self):
        if abs(self.vy) >= self.max_vy:
            self.vy /= abs(self.vy)
            self.vy *= self.max_vy

    def move_y(self):
        self.y += self.vy * self.game.deltatime
        self.vy += self.gravity * self.game.deltatime
        self.rect.y = round(self.y)

    def vertical_collision(self):
        for sprite in collidableObject.CollidableObject.get_collided(self):
            if self.rect.centery < sprite.rect.centery and self.vy > 0:
                self.vy = 0
                self.bottom = sprite.rect.top
            elif self.rect.centery > sprite.rect.centery and self.vy < 0:
                self.vy = 0
                self.top = sprite.rect.bottom

        self.rect.y = round(self.y)
