from functools import wraps


class SkipHandler(object):

    def __init__(self, handler):
        self.handler = handler
        wraps(handler)(self)

    def __call__(self, r, *args, **kwargs):
        if r:
            return self.handler(r, *args, **kwargs)
        else:
            return r

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        new_func = self.handler.__get__(obj, type)
        return self.__class__(new_func)
