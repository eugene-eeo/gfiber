from unittest import main, TestCase
from simplecoro import Fiber, WrongThread, FiberFinished
from threading import Thread, current_thread


class TestFiber(TestCase):
    def test_init(self):
        fiber = Fiber(lambda: [])
        assert fiber.thread is current_thread()
        assert not fiber.done

    def test_switch_simple(self):
        def task():
            array.append(1)
            yield

        array = []
        fiber = Fiber(task)
        fiber.switch()
        assert array == [1]
        assert not fiber.done

    def test_switch_double(self):
        def task():
            array.append(1)
            yield
            array.append(2)

        array = []
        fiber = Fiber(task)
        fiber.switch()
        fiber.switch()
        try:
            fiber.switch()
            assert False
        except FiberFinished:
            assert array == [1, 2]
            assert fiber.done

    def test_throw(self):
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

if __name__ == '__main__':
    main()
