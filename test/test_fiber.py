from pytest import raises
from gfiber import Fiber, FiberFinished
from threading import current_thread


def test_fiber_init():
    fiber = Fiber(lambda: [])
    assert fiber.thread is current_thread()
    assert not fiber.done
    assert not fiber.coro


def test_throw_unfinished():
    def task():
        try:
            yield
            array.append(1)
        except IndexError:
            array.append(2)
            yield

    array = []
    fiber = Fiber(task)
    fiber.switch()
    fiber.throw(IndexError)
    assert array == [2]
    assert not fiber.done


def test_throw_finished():
    def task():
        try:
            yield
        except IndexError:
            pass

    fiber = Fiber(task)
    fiber.switch()
    with raises(StopIteration):
        fiber.throw(IndexError)
