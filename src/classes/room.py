import main
from src.classes.block import *
from src.classes.chunk import *

from random import randint


class Room:
    def __init__(self, game, start_chunk, start_chunk_mask, start_room=False):
        self.chunks = []
        self.out_doors = 0
        self.min_out_doors = randint(2, 4)
        self.new_chunk_chance = 1
        self.start_room = start_room

        self.new_chunks = [(start_chunk, start_chunk_mask)]

        self.game: main.Game = game
        self.max_chunks = randint(5, 10)
        self.min_chunks = 3
        self.n_chunks = 0
        self.generate_room()
        # print('Room generated')

    def next_chunk_is_free(self, direction, pos):

        new_chunk = [(0, -1),
                     (1, 0),
                     (0, 1),
                     (-1, 0)]

        x, y = pos[0] + new_chunk[direction][0], pos[1] + new_chunk[direction][1]
        is_free = True
        for room in self.game.rooms:
            for pos in room.chunks:
                if (pos.x, pos.y) == (x, y):
                    is_free = False
                    break
        return is_free

    def generate_new_chunk(self, chunk):
        chunk_type = list(chunk[1])
        new_chunk = [(0, -1, (0, 0, 2, 0)),
                     (1, 0, (0, 0, 0, 2)),
                     (0, 1, (2, 0, 0, 0)),
                     (-1, 0, (0, 2, 0, 0))]

        for direction in range(len(chunk_type)):
            if chunk_type[direction] == 3:
                chunk_type[direction] = 2
                continue
            if chunk_type[direction] == 0:
                if randint(1, 2) == 1 or self.n_chunks < self.min_chunks:
                    chunk_type[direction] = 2
                    self.new_chunks.append(
                        ((chunk[0][0] + new_chunk[direction][0], chunk[0][1] + new_chunk[direction][1]),
                         (new_chunk[direction][2])))
                elif self.out_doors < 0:
                    chunk_type[direction] = 3
                    self.out_doors += 1
                else:
                    chunk_type[direction] = 1
        self.chunks.append(Chunk(self.game, chunk[0], chunk_type))

    def post_generate_chunks(self, chunks):

        old_chunk = [(0, 1, (0, 0, 2, 0), 0),
                     (-1, 0, (0, 0, 0, 2), 1),
                     (0, -1, (2, 0, 0, 0), 2),
                     (1, 0, (0, 2, 0, 0), 3)]
        for chunk in chunks:
            is_free = True
            for room in self.game.rooms:
                for pos in room.chunks:
                    if (pos.x, pos.y) == chunk[0]:
                        is_free = False
                        break
            for chunk_1 in self.chunks:
                if (chunk_1.x, chunk_1.y) == chunk[0]:
                    is_free = False
                    break
            only_wall = False
            for chunk_2 in self.game.new_rooms_cords:
                if chunk[0] == chunk_2[0]:
                    only_wall = True

            if is_free:
                for i in range(len(old_chunk)):
                    if old_chunk[i][2] == chunk[1]:
                        x, y = chunk[0][0] + old_chunk[i][0], chunk[0][1] + old_chunk[i][1]
                        for j in range(len(self.chunks)):
                            if (self.chunks[j].x, self.chunks[j].y) == (x, y):
                                if self.out_doors < self.min_out_doors and not only_wall:
                                    self.chunks[j].type[old_chunk[i][3]] = 3
                                    self.out_doors += 1
                                    # for direction in range(len(chunk[1])):
                                    #    if chunk[1][direction] == 2:
                                    #        mask = list(chunk[1])
                                    #        mask[direction] = 3
                                    #        chunk = list(chunk)
                                    #        mask = tuple(mask)
                                    #        chunk[1] = mask
                                    #        break
                                    self.chunks[j].doors_start_pos[i] = (chunk[0])
                                    self.game.new_rooms_cords.append(chunk)
                                else:
                                    self.chunks[j].type[old_chunk[i][3]] = 1

                                self.chunks[j].generate_chunk()

    def generate_room(self):
        if self.start_room:
            self.chunks.append(Chunk(self.game, (0, 0), (1, 2, 2, 1)))
            self.chunks.append(Chunk(self.game, (1, 0), (1, 1, 2, 2)))
            self.chunks.append(Chunk(self.game, (0, 1), (2, 2, 1, 3)))
            self.chunks.append(Chunk(self.game, (1, 1), (2, 1, 1, 2)))

            return
        continue_generate = True
        post_chunks = []
        old_chunk = [(0, 1, (0, 0, 2, 0), 0),
                     (-1, 0, (0, 0, 0, 2), 1),
                     (0, -1, (2, 0, 0, 0), 2),
                     (1, 0, (0, 2, 0, 0), 3)]
        while continue_generate:
            continue_generate = False
            n = len(self.new_chunks)
            for i in range(n):
                free_pos = True
                chunk = self.new_chunks[i]
                for room in self.game.rooms:
                    for pos in room.chunks:
                        if (pos.x, pos.y) == chunk[0]:
                            free_pos = False
                            break
                for pos in self.chunks:
                    if (pos.x, pos.y) == chunk[0]:
                        free_pos = False
                        break

                for chunk_2 in self.game.new_rooms_cords:
                    if chunk[0] == chunk_2[0]:
                        post_chunks.append(chunk)
                        free_pos = False
                        break

                if free_pos:
                    self.generate_new_chunk(chunk)
                    self.n_chunks += 1
                    continue_generate = True
                #   else:
                #       for j in range(len(old_chunk)):
                #           if old_chunk[j][2] == chunk[1]:
                #               x, y = chunk[0][0] + old_chunk[j][0], chunk[0][1] + old_chunk[j][1]
                #               for z in range(len(self.chunks)):
                #                   if (self.chunks[z].x, self.chunks[z].y) == (x, y):
                #                       self.chunks[z].type[old_chunk[j][3]] = 1
                #                       self.chunks[z].generate_chunk()
                #                       print('Artur', self.chunks[z].x, self.chunks[z].y, self.chunks[z].type)

            self.new_chunks = self.new_chunks[n:]
            self.new_chunk_chance += 1
            if self.n_chunks >= self.max_chunks:
                continue_generate = False

        # post generate
        self.post_generate_chunks(self.new_chunks + post_chunks)

    def close_room(self):
        next_chunk = [(0, -1, (0, 0, 2, 0), 2),
                      (1, 0, (0, 0, 0, 2), 3),
                      (0, 1, (2, 0, 0, 0), 0),
                      (-1, 0, (0, 2, 0, 0), 1)]
        for chunk in self.chunks:
            for direction in range(len(chunk.type)):
                if chunk.type[direction] == 3:
                    next_chunk_is_door = False
                    x, y = chunk.x + next_chunk[direction][0], chunk.y + next_chunk[direction][1]
                    for room in self.game.rooms:
                        for chunk_1 in room.chunks:
                            if (chunk_1.x, chunk_1.y) == (x, y):
                                if chunk_1.type[next_chunk[direction][3]] != 1:
                                    next_chunk_is_door = True
                                    break
                    if not next_chunk_is_door:
                        mask = list(chunk.type)
                        mask[direction] = 1
                        chunk.type = tuple(mask)
                        chunk.generate_chunk()

    # print('Room closed')

    def delete_room(self):
        old_chunk = [(0, -1, (0, 0, 2, 0), 2),
                     (1, 0, (0, 0, 0, 2), 3),
                     (0, 1, (2, 0, 0, 0), 0),
                     (-1, 0, (0, 2, 0, 0), 1)]
        for chunk in self.chunks:
            for direction in range(len(chunk.type)):
                x, y = chunk.x + old_chunk[direction][0], chunk.y + old_chunk[direction][1]
                for room in self.game.rooms:
                    for other_chunk in room.chunks:
                        if (other_chunk.x, other_chunk.y) == (x, y):
                            if other_chunk.type[old_chunk[direction][3]] == 2:
                                mask = list(other_chunk.type)
                                if chunk.type[direction] == 3:
                                    mask[old_chunk[direction][3]] = 3
                                    other_chunk.doors_start_pos[old_chunk[direction][3]] = (chunk.x, chunk.y)
                                    self.game.new_rooms_cords.append(((chunk.x, chunk.y), old_chunk[direction][2]))
                                elif chunk.type[direction] == 1:
                                    mask[old_chunk[direction][3]] = 1
                                other_chunk.type = mask
                                other_chunk.generate_chunk()
            #print(chunk.blocks)
            for block in chunk.blocks:
                block.destroy()
            # chunk.blocks = []
            #print()
           # print(chunk.blocks)

        for chunk in self.chunks:
            for door_pos in chunk.doors_start_pos:
                if door_pos is not None:
                    for door in self.game.triggers:
                        if door.start_room_pos == door_pos:
                            del self.game.triggers[self.game.triggers.index(door)]
                    for cord in self.game.new_rooms_cords:
                        if cord[0] == door_pos:
                            del self.game.new_rooms_cords[self.game.new_rooms_cords.index(cord)]
