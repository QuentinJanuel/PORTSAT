from time import time


def benchmark(fun, *args, **kwargs):
    start = time()
    fun(*args, **kwargs)
    end = time()
    return end - start
