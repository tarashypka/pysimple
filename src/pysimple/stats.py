import numpy as np


def bootstrap(x: np.array, samples: int=100, percent: int=10) -> (float, float, float):
    """Bootstrap values, return actual mean and (percent / 2, 100 - percent / 2) percentiles"""
    percentiles = (percent / 2, 100 - percent / 2)
    x_mean = np.mean(x)
    x_bootstrapped = np.mean(np.random.choice(x, size=(samples, len(x))), axis=1)
    x_percentile1, x_percentile2 = np.percentile(x_bootstrapped, percentiles)
    return x_mean, x_percentile1, x_percentile2
