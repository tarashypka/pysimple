import multiprocessing as mp
from functools import partial
from typing import *

from tqdm import tqdm


__SENTINEL__ = 1


def _map_func_wrapper(*args, map_func: Callable, que: mp.Queue, **kwargs):
    res = map_func(*args, **kwargs)
    que.put(__SENTINEL__)
    return res


def _tqdm_listener(que: mp.Queue, total: int, bar=tqdm):
    progress_bar = bar(total=total)
    for _ in iter(que.get, None):
        progress_bar.update()


def map_reduce(
        inputs: List, workers: int, map_func: Callable, reduce_func: Callable=None, reduce_init=None, progress_bar=tqdm,
        **map_func_kwargs) -> "output of reduce_func or list of map_func outputs":
    """Standard map-reduce routine to parallellize inputs between workers"""

    if not isinstance(inputs[0], tuple):
        inputs = ((inp,) for inp in inputs)

    if workers > 1:
        que: mp.Queue = None
        tqdm_proc: mp.Process = None
        if progress_bar:
            que = mp.Manager().Queue()
            tqdm_proc = mp.Process(target=_tqdm_listener, args=(que, len(inputs), progress_bar))
            tqdm_proc.start()
            map_func = partial(_map_func_wrapper, map_func=map_func, que=que, **map_func_kwargs)
        else:
            map_func = partial(map_func, **map_func_kwargs)

        with mp.Pool(workers) as p:
            outputs = p.starmap(map_func, inputs)

        if progress_bar:
            que.put(None)
            tqdm_proc.join()
    else:
        if progress_bar:
            inputs = progress_bar(inputs)
        outputs = [map_func(*inp, **map_func_kwargs) for inp in inputs]

    if reduce_func is None:
        return outputs
    else:
        reduced_outp = reduce_func(outputs[0], reduce_init)
        for outp in outputs[1:]:
            reduced_outp = reduce_func(outp, reduced_outp)
        return reduced_outp
