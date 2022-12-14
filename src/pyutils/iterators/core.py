# -*- coding:utf-8 -*-
# @FileName :core.py
# @Author   :Deyu He
# @Time     :2022/8/25 8:49

import copy
import random
from collections.abc import Iterable

__all__ = [
    "make_cyclic_iterator",
]


def make_cyclic_iterator(it, shuffle=True):
    assert isinstance(it, Iterable)
    it = list(it)
    it_ = copy.deepcopy(it)
    if shuffle:
        random.shuffle(it_)
    it_ = iter(it_)
    while True:
        try:
            yield next(it_)
        except StopIteration:
            it_ = copy.deepcopy(it)
            if shuffle:
                random.shuffle(it_)
            it_ = iter(it_)
