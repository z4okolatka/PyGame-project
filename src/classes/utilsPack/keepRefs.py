from collections import defaultdict
import weakref
import main


class KeepRefs:
    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def init_game(cls, game):
        cls.game: main.Game = game

    @classmethod
    def get_refs(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is None:
                cls.__refs__[cls].remove(inst_ref)
                continue
            yield inst

    @classmethod
    def get_allcls_refs(cls):
        for cls_, class_refs in KeepRefs.__refs__.items():
            for inst_ref in class_refs:
                inst = inst_ref()
                if inst is None:
                    cls_.__refs__[cls_].remove(inst_ref)
                    continue
                yield inst