from simplecoro import Fiber
from threading import Thread, Lock


def task1():
    print(1)
    yield f2
    print(3)
    yield f3
    print(6)
    yield f3

def task2():
    print(2)
    yield f1
    print(5)
    yield f1


def task3():
    print(4)
    yield f2
    print(7)


f1 = Fiber(task1)
f2 = Fiber(task2)
f3 = Fiber(task3)

f1.switch()
