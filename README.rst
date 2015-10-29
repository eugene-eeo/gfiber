gfiber
======

An experiment in utilising generators for an extremely lightweight
and cheap "Fiber" implementation, with the ability to context-switch
and throw exceptions already provided by the runtime. Example usage:

.. code-block:: python

    >>> from gfiber import Fiber

    >>> def task1():
            print(1)
            yield f2
            print(3)

    >>> def task2():
            print(2)
            yield f1

    >>> f1 = Fiber(task1)
    >>> f2 = Fiber(task2)
    >>> f1.switch()
    1
    2
    3
