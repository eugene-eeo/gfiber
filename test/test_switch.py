from pytest import raises
from gfiber import Fiber, FiberFinished


def test_switch_simple():
    def task():
        array.append(1)
        yield

    array = []
    fiber = Fiber(task)
    fiber.switch()
    assert array == [1]
    assert not fiber.done


def test_switch_all():
    def task():
        array.append(1)
        yield
        array.append(2)

    array = []
    fiber = Fiber(task)
    fiber.switch()
    fiber.switch()
    assert array == [1, 2]
    assert fiber.done


def test_switch_done():
    def task():
        yield

    fiber = Fiber(task)
    fiber.switch()
    fiber.switch()
    assert fiber.done
    with raises(FiberFinished):
        fiber.switch()