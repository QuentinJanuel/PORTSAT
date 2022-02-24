from random import Random
from time import time


class _ReproducibleRandom:
    def __init__(self, seed):
        self.seed = seed
        self.rd = Random(seed)
        print(f"Initialised {self.__class__.__name__} with seed {self.seed}")

    def random(self):
        return self.rd.random()

    def randint(self, a, b):
        return self.rd.randint(a, b)


# Set a seed for reproducibility
rr = _ReproducibleRandom(int(time() * 100))
