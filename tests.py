from unittest import main, TestCase
from simplecoro import Fiber, WrongThread, FiberFinished
from threading import Thread, Lock, current_thread


class TestFiber(TestCase):
    def test_init(self):
        fiber = Fiber(lambda: [])
        assert fiber.thread is current_thread()

    def test_switch_simple(self):
        def task():
            array.append(1)
            yield

        array = []
        fiber = Fiber(task)
        fiber.switch()
        assert array == [1]

    def test_switch_double(self):
        def task():
            yield

        fiber = Fiber(task)
        fiber.switch()
        try:
            fiber.switch()
            assert False
        except FiberFinished:
            pass


if __name__ == '__main__':
    main()
