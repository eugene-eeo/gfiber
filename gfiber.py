from threading import current_thread


class WrongThread(Exception):
    pass


class FiberFinished(Exception):
    pass


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
