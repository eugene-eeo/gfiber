from threading import current_thread
from .utils import guard
from .exceptions import FiberFinished


class Fiber(object):
    def __init__(self, task):
        self.coro = task()
        self.thread = current_thread()

    def switch(self):
        with guard(self.thread):
            for fiber in self.coro:
                if fiber is not None:
                    fiber.switch()
                return
            raise FiberFinished
