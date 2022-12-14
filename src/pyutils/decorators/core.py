# -*- coding:utf-8 -*-
# @FileName :core.py
# @Author   :Deyu He
# @Time     :2022/8/23 10:33


from functools import wraps

__all__ = [
    "set_member_variables",
    "set_class_variables",
]


def set_member_variables(variable_dict, force=True):
    """
    Set member variables for an instance after its __init__ method is called.
    :param variable_dict:
    :param force:
    :return:
    """

    def wrapped_func(func):
        @wraps(func)
        def inner_wrapped_func(*args, **kwargs):
            obj = func(*args, **kwargs)
            for k, v in variable_dict.items():
                if hasattr(obj, k) and not force:
                    continue
                setattr(obj, k, v)
            return obj

        return inner_wrapped_func

    return wrapped_func


def set_class_variables(variable_dict, force=True):
    """
    Set class variables for a class.
    :param variable_dict:
    :param force:
    :return:
    """

    def wrapped_func(cls):
        for k, v in variable_dict.items():
            if hasattr(cls, k) and not force:
                continue
            setattr(cls, k, v)
        return cls

    return wrapped_func
