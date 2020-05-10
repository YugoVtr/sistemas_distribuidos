def coroutine(fn):
    def wrapper(*args, **kwargs):
        c = fn(*args, **kwargs)
        next(c)
        return c
    return wrapper