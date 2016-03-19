from pytest import raises
from gfiber import Fiber, FiberFinished, WrongThread
from exthread import ExThread


def test_switch():
    def task():
        arr.append(1)
        yield
        arr.append(2)

    arr = []
    fiber = Fiber(task)
    fiber.switch()
    assert arr == [1]
    assert not fiber.done

    fiber.switch()
    assert arr == [1, 2]
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
        yield

    def assertion():
        with raises(WrongThread):
            fiber.switch()

    fiber = Fiber(task)
    thread = ExThread(assertion)
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
