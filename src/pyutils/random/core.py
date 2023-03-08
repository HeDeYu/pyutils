import numpy as np

__all__ = [
    "random_normal",
]


def random_normal(m=0.0, std=1.0, clip=None):
    ret = np.random.normal(loc=m, scale=std)
    print(ret)
    if clip is not None:
        if ret - m > clip * std:
            return m + clip * std
        elif m - ret > clip * std:
            return m - clip * std
    return ret
