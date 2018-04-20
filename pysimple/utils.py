from typing import *

import datetime as dt


def silent(*args, **kwargs) -> None:
    return


def is_hash(h: str) -> bool:
    return h.isdigit() or (h.startswith('-') and h[1:].isdigit())


def now() -> str:
    return dt.datetime.now().strftime("%y%m%d%H%M%S")


def rm_oob_samples(x: List[Any], batch_size: int) -> List[Any]:
    """Remove out of batch samples"""
    n_oob = len(x) % batch_size
    if n_oob > 0:
        x = x[:-n_oob]
    return x
