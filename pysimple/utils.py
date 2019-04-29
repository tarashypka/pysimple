from ctypes import c_long
from typing import *

import numpy as np
import pandas as pd
from cityhash import CityHash64


def flatten_iter(x: Iterator[Iterator[Any]]) -> Iterator[Any]:
    """Flatten list or set"""
    return (item for items in x for item in items)


def df2dict(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert pandas DataFrame rows into list of records."""
    return list(data.T.to_dict().values())


def split_list(
        items: List[Any], splits: List[int]=None, n_splits: int=None, split_size: int=None) -> Iterator[List[Any]]:
    """Split list into sub-lists of equal size or into sub-lists of specific length, preserves order of elements"""
    items = list(items)
    n_items = len(items)

    if splits is not None:
        split_pos = [0] + splits + [n_items]
    elif n_splits is not None or split_size is not None:
        all_pos = np.arange(n_items)
        if split_size is None:
            split_size = n_items // n_splits
        split_pos = all_pos[::split_size].tolist() + [n_items]
    else:
        raise TypeError('Must pass either splits, or n_splits!')

    for _pos, pos_ in zip(split_pos[:-1], split_pos[1:]):
        yield items[_pos:pos_]


def data2batches(
        data: pd.DataFrame, n_batches: int=None, batch_size: int=None,
        orient: str=None) -> Iterator[Union[List[Dict[str, Any]], pd.DataFrame]]:
    """Split data table into batches of tables or records"""
    if batch_size is None:
        batch_size = np.ceil(len(data) / n_batches)
    if orient is None:
        bins = np.arange(len(data)) // batch_size
        for _, batch in data.groupby(bins):
            yield batch
    else:
        if orient == 'records':
            data = df2dict(data=data)
            n_splits = int(np.ceil(len(data) / batch_size))
            yield from split_list(items=data, n_splits=n_splits)
        else:
            raise ValueError(f'Invalid value of orient = {orient}, must be one of "records,None"!')


def compute_hash64(text: Union[str, pd.Series]) -> Union[int, pd.Series]:
    """Compute consistent 64-bit signed integer for text or texts"""
    if isinstance(text, str):
        text_hash = c_long(CityHash64(text)).value
    elif isinstance(text, pd.Series):
        text_hash = text.apply(CityHash64)
        text_hash = text_hash.astype(np.int64) if text_hash.dtype == np.uint64 else text_hash
        if text_hash.dtype != np.int64:
            raise ValueError(f'Computed hashes must be of type np.int64 instead of {text_hash.dtype}!')
    else:
        raise TypeError(f"Input must of type str or Series, but got {type(text)}!")
    return text_hash
