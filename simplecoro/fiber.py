from threading import current_thread
from .exceptions import FiberFinished


class Fiber(object):
    def __init__(self, task):
        self.coro = task()
        self.done = False
        self.thread = current_thread()

    def guard(self):
        if current_thread() != self.thread:
            raise WrongThread
        if self.done:
            raise FiberFinished

    def switch(self):
        self.guard()
        for fiber in self.coro:
            if fiber is not None:
                fiber.switch()
            return
        self.done = True

    def throw(self, *exc):
        self.guard()
        self.coro.throw(*exc)
