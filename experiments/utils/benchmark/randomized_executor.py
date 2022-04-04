from typing import Any, Callable, List, Tuple, Generic, TypeVar
from utils.reprandom import rr
from utils.progress import Progress

T = TypeVar("T")


class Job(Generic[T]):
    def __init__(
        self,
        fun: Callable[..., T],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._fun = fun
        self._args = args
        self._kwargs = kwargs

    def run(self) -> T:
        return self._fun(*self._args, **self._kwargs)


class RandomizedExecutor(Generic[T]):
    def __init__(self, repetitions: int = 1):
        self._jobs: List[Tuple[str, Job[T]]] = []
        self._results: List[Tuple[str, T]] = []
        self._repetitions: int = repetitions
        self._has_run: bool = False
        self._results_dict: dict = {}

    def add(self, key: str, job: Job[T]):
        for _ in range(self._repetitions):
            self._jobs.append((key, job))

    def exec_all(self, verbose: bool = True) -> None:
        if self._has_run:
            raise Exception(" ".join([
                "Cannot exec_all because",
                "this executor has already been ran",
            ]))
        rr.shuffle(self._jobs)
        progress = Progress("Execution", len(self._jobs))
        for cur_prog, (key, job) in enumerate(self._jobs):
            result = job.run()
            self._results.append((key, result))
            if verbose:
                progress.log(cur_prog + 1)
        if verbose:
            progress.end()
        self._has_run = True

    def get_results(self, key: str) -> List[T]:
        results: List[T] = []
        for key2, result in self._results:
            if key == key2:
                results.append(result)
        return results
