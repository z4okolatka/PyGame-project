import pygame as pg
from src.classes.utilsPack import coordHelper
import weakref


class CollidableObject(coordHelper.FloatCords):
    __refs__ = []

    @classmethod
    def get_refs(cls):
        for obj in cls.__refs__:
            inst_obj = obj()
            if inst_obj is None:
                cls.__refs__.remove(obj)
                continue
            yield inst_obj
    
    @classmethod
    def get_collided(cls, sprite):
        for obj in cls.__refs__:
            inst_obj = obj()
            if inst_obj is None:
                cls.__refs__.remove(obj)
                continue
            if inst_obj.is_colliding(sprite):
                yield inst_obj

    def __init__(self):
        super().__init__()
        CollidableObject.__refs__.append(weakref.ref(self))
    
    def is_colliding(self, sprite):
        return self.rect.colliderect(sprite)