import datetime as dt
import hashlib
from ctypes import c_long
from pathlib import Path
from typing import *

import numpy as np
import pandas as pd
from cityhash import CityHash64

from pysimple.io import plain_path


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


DT_TYPE = Union[dt.date, dt.datetime]


def diff_between_dates(from_date: DT_TYPE, till_date: DT_TYPE, delta: str) -> int:
    """Count delta between dates, both from_date and till_date must be of the same type"""
    diff = till_date - from_date
    seconds = diff.days * 24 * 60 * 60 + diff.seconds
    if delta == 'day':
        period = 60 * 60 * 24
    elif delta == 'hour':
        period = 60 * 60
    elif delta == 'min':
        period = 60
    elif delta == 'sec':
        period = 1
    else:
        raise ValueError(f'Unknown delta={delta}, must be one of day,hour,min,sec!')
    return seconds // period


def get_dates_between(start_date: DT_TYPE, end_date: DT_TYPE, **delta_args) -> Iterator[DT_TYPE]:
    """Get list of dates between start and end dates"""
    if not delta_args:
        raise ValueError('Must pass one of datetime deltas: days,hours,minutes,seconds,...!')
    curr_date = start_date
    while curr_date < end_date:
        yield curr_date
        curr_date += dt.timedelta(**delta_args)


def get_checksum(*, text: str=None, filepath: Path=None, encoding: str='UTF-8', errors: str='strict') -> int:
    """Calculate checksum of file or text"""
    if filepath is not None:
        text = plain_path(filepath).read_bytes()
    else:
        text = bytes(text, encoding=encoding, errors=errors)
    return hashlib.md5(text).hexdigest()


def get_tmp_col(df: pd.DataFrame) -> str:
    """Get temporary column name to avoid name collisions"""
    ind_col = 'tmp_col_'
    while True:
        if ind_col not in df.columns:
            break
        ind_col += '_'
    return ind_col


def split_into_batches(data: pd.DataFrame, split_cols: List[str], n_batches: int) -> Iterator[pd.DataFrame]:
    """Split data table into batches with non-overlapping column values"""
    ind_col = get_tmp_col(df=data)
    data[ind_col] = data.groupby(split_cols).ngroup()
    group_inds = data[ind_col].unique().tolist()
    group_inds = split_list(items=group_inds, n_splits=n_batches)
    for inds in group_inds:
        yield data[data[ind_col].isin(inds)].drop(columns=[ind_col])


def cumsplit(items: List[Union[int, float]], n_splits: int) -> List[int]:
    """
    Get positions at which to split array into sub-arrays of equal sum.
    Possible use-case is when items are lengths of batches to split them into chunks of equal computational complexity.
    """
    # Sum of elements: should be equal for each sub-array
    items = sorted(items)
    chunk_weight = np.sum(items) / n_splits
    cumitems = np.cumsum(items)
    pos = []
    # n-1 divisions for n sub-arrays
    for i in range(1, n_splits):
        new_pos = np.where(cumitems >= chunk_weight * i)[0][0]
        if new_pos not in pos:
            pos.append(new_pos)
    return pos
