import src.setting
from src.classes.mapPack.block import Block
from src.classes.mapPack import door
import main


class Chunk:
    def __init__(self, game, cords, chunk_type):
        self.x, self.y = cords
        self.size = src.setting.CHUNK_SIZE
        self.out_door_size = src.setting.CHUNK_OUT_DOOR_SIZE
        self.type = chunk_type
        '''
        1 - wall
        2 - door to the next chunk
        3 - door to the next room
        
        self.type[0] - TOP
        self.type[1] - RIGHT
        self.type[2] - BOTTOM
        self.type[3] - LEFT
        '''
        self.game: main.Game = game
        self.blocks = []
        self.doors = []
        self.doors_start_pos = [None, None, None, None]
        self.generate_chunk()

    def delete_blocks(self):
        for block in self.blocks:
            try:
                block.destroy()
            except:
                pass

    def generate_chunk(self):
        self.delete_blocks()
        if self.type[0] == 1:
            self.blocks.append(
                Block((self.x * self.size, self.y * self.size - self.size // 2), (self.size, 10)))
        elif self.type[0] == 3:
            self.blocks.append(
                Block((self.x * self.size - self.out_door_size // 2 - ((self.size - self.out_door_size) // 4),
                       self.y * self.size - self.size // 2), ((self.size - self.out_door_size) // 2, 10)))
            self.blocks.append(
                Block((self.x * self.size + self.out_door_size // 2 + ((self.size - self.out_door_size) // 4),
                       self.y * self.size - self.size // 2), ((self.size - self.out_door_size) // 2, 10)))

        if self.type[1] == 1:
            self.blocks.append(
                Block((self.x * self.size + self.size // 2, self.y * self.size), (10, self.size)))
        elif self.type[1] == 3:
            self.blocks.append(
                Block((self.x * self.size + self.size // 2,
                       self.y * self.size - self.out_door_size // 2 - (self.size - self.out_door_size) // 4),
                      (10, (self.size - self.out_door_size) // 2)))
            self.blocks.append(
                Block((self.x * self.size + self.size // 2,
                       self.y * self.size + self.out_door_size // 2 + (self.size - self.out_door_size) // 4),
                      (10, (self.size - self.out_door_size) // 2)))

        if self.type[2] == 1:
            self.blocks.append(
                Block((self.x * self.size, self.y * self.size + self.size // 2), (self.size, 10)))
        elif self.type[2] == 2:
            self.blocks.append(
                Block((self.x * self.size, self.y * self.size), (100, 30)))
        elif self.type[2] == 3:
            self.blocks.append(
                Block((self.x * self.size - self.out_door_size // 2 - ((self.size - self.out_door_size) // 4),
                       self.y * self.size + self.size // 2), ((self.size - self.out_door_size) // 2, 10)))
            self.blocks.append(
                Block((self.x * self.size + self.out_door_size // 2 + ((self.size - self.out_door_size) // 4),
                       self.y * self.size + self.size // 2), ((self.size - self.out_door_size) // 2, 10)))

        if self.type[3] == 1:
            self.blocks.append(
                Block((self.x * self.size - self.size // 2, self.y * self.size), (10, self.size)))
        elif self.type[3] == 3:
            self.blocks.append(
                Block((self.x * self.size - self.size // 2,
                       self.y * self.size - self.out_door_size // 2 - (self.size - self.out_door_size) // 4),
                      (10, (self.size - self.out_door_size) // 2)))
            self.blocks.append(
                Block((self.x * self.size - self.size // 2,
                       self.y * self.size + self.out_door_size // 2 + (self.size - self.out_door_size) // 4),
                      (10, (self.size - self.out_door_size) // 2)))
        # print(self.doors_start_pos)
        if self.doors_start_pos[0] is not None:
            self.doors.append(
            door.Door((self.x * self.size, self.y * self.size - self.size // 2), (self.out_door_size, 10),
                 self.doors_start_pos[0]))
        if self.doors_start_pos[1] is not None:
            self.doors.append(
            door.Door((self.x * self.size + self.size // 2, self.y * self.size), (10, self.out_door_size),
                 self.doors_start_pos[1]))
        if self.doors_start_pos[2] is not None:
            self.doors.append(
            door.Door((self.x * self.size, self.y * self.size + self.size // 2), (self.out_door_size, 10),
                 self.doors_start_pos[2]))
        if self.doors_start_pos[3] is not None:
            self.doors.append(
            door.Door((self.x * self.size - self.size // 2, self.y * self.size), (10, self.out_door_size),
                 self.doors_start_pos[3]))
