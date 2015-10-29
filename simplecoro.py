from contextlib import contextmanager
from threading import current_thread


class WrongThread(Exception):
    pass


@contextmanager
def guard(thread):
    if current_thread() != thread:
        raise WrongThread
    yield


class Fiber(object):
    def __init__(self, task):
        self.coro = task()
        self.thread = current_thread()

    def switch(self):
        with guard(self.thread):
            for fiber in self.coro:
                if fiber is None:
                    break
                fiber.switch()
                return
