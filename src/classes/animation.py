from PIL import Image
import pygame as pg


class Animation:
    def __init__(self, path_to_gif):
        self.path = path_to_gif
        self.images = []
        self.unpack_gif(self.path)

        self.animationFrameIndex = 0
        self.animTime = 0

        self.image = self.images[self.animationFrameIndex][0]

    def unpack_gif(self, path):
        imageSequence = Image.open(path)
        self.animationLen = imageSequence.n_frames - 1
        for frame_ind in range(1, self.animationLen + 1):
            imageSequence.seek(frame_ind)
            mode = imageSequence.mode
            size = imageSequence.size
            data = imageSequence.tobytes()
            self.images.append((pg.image.frombytes(
                data, size, mode).convert_alpha(), imageSequence.info['duration']))

    @property
    def animationTime(self):
        return self.animTime

    @animationTime.setter
    def animationTime(self, n):
        self.animTime = n
        if self.animTime >= (dur := self.images[self.animationFrameIndex][1]):
            self.animTime -= dur
            self.animationFrameIndex = (self.animationFrameIndex + 1) % self.animationLen
            self.image = self.images[self.animationFrameIndex][0]