import numpy as np


def bootstrap(x: np.array, samples: int=30) -> np.array:
    """Bootstrap values and compute mean of each sample"""
    xb = np.random.choice(x, size=(samples, len(x)))
    return xb.mean(axis=1)
