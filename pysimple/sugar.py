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


class CachedObject:
    """Context manager that holds object with attribute that may be cached"""

    def __init__(self, obj: object, field: str):
        self.obj = obj
        self.field = field
        self.cache_ = None

    def __enter__(self):
        self.cache_ = getattr(self.obj, self.field)
        setattr(self.obj, self.field, None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self.obj, self.field, self.cache_)

    @staticmethod
    def parse_from(obj: object, field: str):
        fields = field.split('.')
        cache_obj = obj
        cache_name = field
        for inner_obj, inner_name in zip(fields[:-1], fields[1:]):
            cache_obj = getattr(cache_obj, inner_obj)
            cache_name = inner_name
        return CachedObject(obj=cache_obj, field=cache_name)


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


def ignore_warnings(func: Callable) -> Callable:
    """Decorator to ignore all warnings for the moment of function call"""
    def func_without_warnings(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            func(*args, **kwargs)
    return func_without_warnings


def with_seaborn(plot_func: Callable) -> Callable:
    import seaborn as sb

    def reset():
        sb.reset_orig()
        sb.set()
        sb.set_style('whitegrid')

    def plot_func_wrapper(*args, **kwargs):
        reset()
        plot_func(*args, **kwargs)
        reset()

    return plot_func_wrapper
