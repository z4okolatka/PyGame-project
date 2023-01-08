import pygame as pg
from src.classes.mapPack import room, trigger

class Door(trigger.Trigger):
    def __init__(self, centerpos, size, start_room_pos):
        super().__init__(centerpos, size)
        self.start_room_pos = start_room_pos

    def action(self):
        for new_room in self.game.new_rooms_cords:
            if new_room[0] == self.start_room_pos:
                del self.game.new_rooms_cords[self.game.new_rooms_cords.index(new_room)]
                self.game.rooms.append(room.Room(self.game, new_room[0], new_room[1]))
                print(f'Triggered {self}')

        if len(self.game.rooms) > 5:
            self.game.rooms[0].delete_room()
            self.game.rooms = self.game.rooms[1:]
        if len(self.game.rooms) == 5:
            self.game.rooms[0].close_room()


