from threading import current_thread
from .utils import guard
from .exceptions import FiberFinished


class Fiber(object):
    def __init__(self, task):
        self.coro = task()
        self.done = False
        self.thread = current_thread()

    def switch(self):
        with guard(self.thread):
            if self.done:
                raise FiberFinished
            for fiber in self.coro:
                if fiber is not None:
                    fiber.switch()
                return
            self.done = True
