import numpy as np


def bootstrap(x: np.array, samples: int=100, percent: int=10) -> (float, float, float):
    """Bootstrap values, return actual mean and bootstrap percentiles"""
    percentiles = (percent / 2, 100 - percent / 2)
    x_mean = np.mean(x)
    x_bootstrapped = np.mean(np.random.choice(x, size=(samples, len(x))), axis=1)
    x_percentile_small, x_percentile_large = np.percentile(x_bootstrapped, percentiles)
    return x_mean, x_percentile_small, x_percentile_large
