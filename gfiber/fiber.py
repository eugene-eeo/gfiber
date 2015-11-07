from .exceptions import FiberFinished


class Fiber(object):
    def __init__(self, task):
        self.coro = iter(task())
        self.done = False

    def guard(self):
        if self.done:
            raise FiberFinished

    def switch(self):
        self.guard()
        try:
            fiber = next(self.coro)
            if fiber is not None:
                fiber.switch()
        except StopIteration:
            self.done = True

    def throw(self, *exc):
        self.guard()
        try:
            self.coro.throw(*exc)
        except StopIteration:
            self.done = True
            raise
