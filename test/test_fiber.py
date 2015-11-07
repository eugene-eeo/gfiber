from pytest import raises
from gfiber import Fiber, FiberFinished


def test_fiber_init():
    fiber = Fiber(lambda: [])
    assert not fiber.done


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
