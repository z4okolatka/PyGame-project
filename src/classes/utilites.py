def absmax(min_, value):
    if not value:
        return 0
    absolute = abs(value)
    sign = value / absolute
    return sign * max(min_, absolute)

def absmin(value, max_):
    if not value:
        return 0
    absolute = abs(value)
    sign = value / absolute
    return sign * min(max_, absolute)