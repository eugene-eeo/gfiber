from pytest import raises
from gfiber import Fiber, FiberFinished, WrongThread
from exthread import ExThread


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


def test_switch_from_different_thread():
    def task():
        yield

    def assertion():
        with raises(WrongThread):
            fiber.switch()

    fiber = Fiber(task)
    thread = ExThread(target=assertion)
    thread.start()
    thread.join()


def test_switch_multiple():
    def t1():
        yield f2
        yield f2

    def t2():
        arr.append(1)
        yield f1
        arr.append(2)

    arr = []
    f1 = Fiber(t1)
    f2 = Fiber(t2)
    f1.switch()
    assert arr == [1,2]
    assert f2.done
