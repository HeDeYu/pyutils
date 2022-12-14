# -*- coding:utf-8 -*-
# @FileName :core.py
# @Author   :Deyu He
# @Time     :2022/7/20 10:15

__all__ = [
    "check_attr_in_list",
    "check_isinstance",
    "check_in_list",
    "make_list",
]


def check_in_list(_values, *, _print_supported_values=True, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is in *_values*.

    Args:
        _values : iterable
            Sequence of values to check on.
        _print_supported_values : bool, default: True
            Whether to print *_values* when raising ValueError.
        **kwargs : dict
            *key, value* pairs as keyword arguments to find in *_values*.

    Raises:
        ValueError: If any *value* in *kwargs* is not found in *_values*.

    Returns:
    >>> check_in_list(["foo", "bar"], arg=arg, other_arg=other_arg)
    """
    values = _values
    for key, val in kwargs.items():
        if val not in values:
            if _print_supported_values:
                raise ValueError(
                    f"{val!r} is not a valid value for {key}; "
                    f"supported values are {', '.join(map(repr, values))}"
                )
            else:
                raise ValueError(f"{val!r} is not a valid value for {key}")


def check_attr_in_list(
    attr_name: str, valid_values, *, _print_supported_values=True, **kwargs
):
    """

    For each *key, value* pair in *kwargs*, check the attribute *value*.*attr_name* is valid

    Args:
        attr_name(str): name of the attribute to be checked.
        valid_values: list
            Sequence of valid values of *attr_name*.
        _print_supported_values : bool, default: True
            Whether to print *_values* when raising ValueError.

        **kwargs : dict
            *key, value* pairs as keyword arguments to find in *_values*.

    Raises:
        ValueError: If the attributes of any *value* in *kwargs* checking failed

    Examples:
        >>> check_attr_in_list('arrti_name', valid_values=[v1], test_1=test_1, test_2=test_2)
        >>> check_attr_in_list('arrti_name', valid_values=[v1, v2], test_1=test_1, test_2=test_2)

    """

    item_value_strs = list(map(str, valid_values))
    if len(item_value_strs) > 1:
        valid_str = ", ".join(item_value_strs[:-1]) + " or " + item_value_strs[-1]
    else:
        valid_str = item_value_strs[0]

    for arg_k, arg_v in kwargs.items():
        attr_value = getattr(arg_v, attr_name)

        if attr_value not in valid_values:

            if _print_supported_values:
                raise ValueError(
                    f"expect attribute {attr_name} to be {valid_str}, "
                    f"while the {attr_name} of {arg_k!r} is {attr_value}"
                )

            else:
                raise ValueError(
                    f"attribute value {attr_value} of {arg_k!r} is not valid"
                )


def check_isinstance(_types, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is an instance
    of one of *_types*; if not, raise an appropriate TypeError.

    As a special case, a ``None`` entry in *_types* is treated as NoneType.

    Examples:
    >>> check_isinstance((SomeClass, None), arg=arg)
    """
    types = _types
    none_type = type(None)
    types = (
        (types,)
        if isinstance(types, type)
        else (none_type,)
        if types is None
        else tuple(none_type if tp is None else tp for tp in types)
    )

    def type_name(tp):
        return (
            "None"
            if tp is none_type
            else tp.__qualname__
            if tp.__module__ == "builtins"
            else f"{tp.__module__}.{tp.__qualname__}"
        )

    for k, v in kwargs.items():
        if not isinstance(v, types):
            names = [*map(type_name, types)]
            if "None" in names:  # Move it to the end for better wording.
                names.remove("None")
                names.append("None")
            raise TypeError(
                "{!r} must be an instance of {}, not a {}".format(
                    k,
                    ", ".join(names[:-1]) + " or " + names[-1]
                    if len(names) > 1
                    else names[0],
                    type_name(type(v)),
                )
            )


def make_list(input):
    if not isinstance(input, (list, tuple)):
        return [input]
    return input
