from math import floor


class Progress:
    def __init__(self, name: str, total: float):
        self._name = name
        self._total = total

    def log(self, current: float):
        percent = floor(current * 100 / self._total)
        content = f"{self._name}: {percent}%"
        print(f"\r{content}" + " " * 10, end="")

    def end(self):
        print()
