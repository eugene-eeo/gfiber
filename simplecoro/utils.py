from threading import current_thread
from contextlib import contextmanager
from .exceptions import WrongThread


@contextmanager
def guard(thread):
    if current_thread() != thread:
        raise WrongThread
    yield
