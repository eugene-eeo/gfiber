from inspect import isgenerator
from contextlib import contextmanager
from threading import current_thread


class WrongThread(Exception):
    pass


@contextmanager
def guard(thread):
    if current_thread() != thread:
        raise WrongThread
    yield


def normalise_task(res):
    if isgenerator(res):
        for item in res:
            yield item


class Fiber(object):
    def __init__(self, task):
        self.task = task
        self.coro = None
        self.thread = current_thread()

    def ensure_start(self):
        if not self.coro:
            self.coro = normalise_task(self.task())

    def switch(self):
        self.ensure_start()
        with guard(self.thread):
            for fiber in self.coro:
                fiber.switch()
                return
