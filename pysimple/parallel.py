import multiprocessing as mp
from functools import partial
from typing import *
from tqdm import tqdm


__SENTINEL__ = 1


def _map_func_wrapper(*args, map_func: Callable, que: mp.Queue, **kwargs):
    res = map_func(*args, **kwargs)
    que.put(__SENTINEL__)
    return res


def _tqdm_listener(que: mp.Queue, total: int):
    progress_bar = tqdm(total=total)
    for _ in iter(que.get, None):
        progress_bar.update()


def map_reduce(
        inputs: List, workers: int, map_func: Callable, reduce_func: Callable=None,
        reduce_init=None, **map_func_kwargs):

    que = mp.Manager().Queue()
    tqdm_proc = mp.Process(target=_tqdm_listener, args=(que, len(inputs)))
    tqdm_proc.start()

    map_func = partial(_map_func_wrapper, map_func=map_func, que=que, **map_func_kwargs)

    with mp.Pool(workers) as p:
        if isinstance(inputs[0], tuple):
            outputs = p.starmap(map_func, inputs)
        else:
            outputs = p.starmap(map_func, ((inp,) for inp in inputs))

    que.put(None)
    tqdm_proc.join()

    if reduce_func is None:
        return outputs
    else:
        reduced_outp = reduce_func(outputs[0], reduce_init)
        for outp in outputs[1:]:
            reduced_outp = reduce_func(outp, reduced_outp)
        return reduced_outp


