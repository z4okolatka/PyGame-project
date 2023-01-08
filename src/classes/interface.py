import main

class UI:
    def __init__(self, game):
        self.game: main.Game = game
    
    def draw_all(self):
        self.draw(self.game.player.inventory)
        # self.draw()
    
    def draw(self, sprite):
        self.game.camera.display.blit(
            sprite.image, sprite.rect
        )