import pygame as pg
from src.classes.coordHelper import FloatCords


class collidableObject(FloatCords):
    __refs__ = []

    @classmethod
    def get_refs(cls):
        return cls.__refs__
    
    @classmethod
    def check_all_collisions(cls, sprite):
        return list(object_ for object_ in cls.__refs__ if object_.colliding(sprite))
    
    def colliding(self, sprite):
        return self.rect.colliderect(sprite)

    def __init__(self):
        super().__init__()
        collidableObject.__refs__.append(self)
    
    def destroy(self):
        self.__class__.__refs__.remove(self)
