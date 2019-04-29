import warnings
from typing import *

import pandas as pd


class ChainedAssignment:
    """Context manager for handling pandas chained assignment warning"""

    acceptable = [None, 'warn', 'raise']

    def __init__(self, action: str=None):
        if action not in ChainedAssignment.acceptable:
            raise AttributeError(f'Invalid value of chained, must be one of {ChainedAssignment.acceptable}!')
        self.action = action
        self.previous_: str = None

    def __enter__(self):
        self.previous_ = pd.options.mode.chained_assignment
        pd.options.mode.chained_assignment = self.action
        return self

    def __exit__(self, *args):
        pd.options.mode.chained_assignment = self.previous_


def ignore_pandas_chained_assignment(func: Callable) -> Callable:
    """Decorator to ignore pandas chained assignment for a while"""
    def func_with_ignored_chained(*args, **kwargs):
        previous = pd.options.mode.chained_assignment
        pd.options.mode.chained_assignment = None
        res = func(*args, **kwargs)
        pd.options.mode.chained_assignment = previous
        return res
    return func_with_ignored_chained


def warn_deprecated(func: Callable) -> Callable:
    """Decorator for deprecated functions"""
    def func_with_deprecated_warning(*args, **kwargs):
        warnings.warn(
            message=f'Function {func.__name__} is deprecated and will be removed later!', category=UserWarning)
        return func(*args, **kwargs)
    return func_with_deprecated_warning
