import pygame as pg

def absmax(min_, value):
    if not value:
        return min_
    absolute = abs(value)
    sign = value / absolute
    return sign * max(min_, absolute)


def absmin(value, max_):
    if not value:
        return value
    absolute = abs(value)
    sign = value / absolute
    return sign * min(max_, absolute)


def clamp(min_, value, max_):
    return max(min_, min(value, max_))


def absclamp(min_, value, max_):
    print(min_, value, max_)
    if not value:
        return value
    absolute = abs(value)
    sign = value / absolute
    return sign * max(min_, min(absolute, max_))

def scale_by(image, value):
    w, h = image.get_size()
    w *= value
    h *= value
    return pg.transform.scale(image, (w, h))