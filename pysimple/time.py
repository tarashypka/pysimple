from time import perf_counter


class Stopwatch:
    """Simple stopwatch to measure elapsed time. May be used both in sync and async."""

    def __init__(self):
        self.started_at_: float = None
        self.stopped_at_: float = None

    def __enter__(self):
        self.started_at_ = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.started_at_ = perf_counter()

    def elapsed_ms(self) -> int:
        """How much time passed in milliseconds since stopwatch started"""
        if not self.started_at_:
            raise ValueError('Stopwatch was not started!')
        if not self.stopped_at_:
            # Stop now, may be stopped later again
            self.stopped_at_ = perf_counter()
        return int(1000 * (self.stopped_at_ - self.started_at_))
