from unittest import main, TestCase
from simplecoro import Fiber, WrongThread
from threading import Thread, Lock, current_thread


class TestFiberBase(TestCase):
    def setUp(self):
        self.arr = []
        def task():
            self.arr.append(1)
        self.fiber = Fiber(task)

    def test_thread(self):
        assert self.fiber.thread == current_thread()

    def test_switch(self):
        self.fiber.switch()
        assert self.arr == [1]


class TestContext(TestCase):
    def test_yield_from_coro(self):
        arr = []
        def task1():
            arr.append(1)
            yield f2
            arr.append(3)

        def task2():
            arr.append(2)
            yield f1

        f1 = Fiber(task1)
        f2 = Fiber(task2)
        f1.switch()
        assert arr == [1,2,3]

    def test_yield_unfinished(self):
        arr = []
        def task1():
            arr.append(1)
            yield f2
            arr.append(3)

        def task2():
            arr.append(2)

        f1 = Fiber(task1)
        f2 = Fiber(task2)
        f1.switch()
        assert arr == [1,2]


class TestConcurrent(TestCase):
    def test_switch(self):
        res = []
        lock = Lock()
        fibers = []

        def switch_f1():
            with lock:
                f1 = Fiber(lambda: [])
                f1.switch()
                fibers.append(f1)

        def switch_f1_again():
            try:
                fibers[0].switch()
            except WrongThread as exc:
                res.append(1)

        threads = [
            Thread(target=switch_f1),
            Thread(target=switch_f1_again),
            ]
        [t.start() for t in threads]
        [t.join() for t in threads]
        assert res == [1]


if __name__ == '__main__':
    main()
