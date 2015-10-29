from contextlib import contextmanager
from threading import current_thread


@contextmanager
def ensure(thread):
    if current_thread() != thread:
        raise Exception
    yield


class Fiber(object):
    def __init__(self, task):
        self.coro = task()
        self.thread = current_thread()
        self.guard = ThreadGuard(self.thread)

    def switch(self):
        with ensure(self.thread):
            for fiber in self.coro:
                fiber.switch()
                return
