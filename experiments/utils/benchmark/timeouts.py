class Timeouts:
    def __init__(self, timeout: float):
        self._solvers = {}
        self._timeout = timeout

    def _get(self, solver: str):
        if solver not in self._solvers:
            return 0
        return self._solvers[solver]

    def new_result(self, solver: str, time: float):
        has_timeout = time > self._timeout
        incr = 1 if has_timeout else 0
        self._solvers[solver] = self._get(solver) + incr

    def __str__(self):
        text = f"Timeout: {self._timeout}s\n"
        text += "Timeout count:\n"
        for solver in self._solvers:
            text += f"{solver}: {self._get(solver)}\n"
        return text
