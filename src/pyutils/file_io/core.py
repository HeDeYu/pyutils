# -*- coding:utf-8 -*-
# @FileName :core.py
# @Author   :Deyu He
# @Time     :2022/7/11 12:39

import json
import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterator, List, Union

import yaml
from loguru import logger

__all__ = [
    "mkdir",
    "append_file_name",
    "replace_parent",
    "copy_related_files",
    "glob_dir",
    "load_xml",
    "dump_xml",
    "load_yaml",
    "dump_yaml",
    "load_json",
    "dump_json",
]


def mkdir(path, parents=True, exist_ok=True):
    Path(str(path)).mkdir(parents=parents, exist_ok=exist_ok)


def append_file_name(path_, append_str):
    path_ = Path(path_)
    return str(path_.parent / Path(path_.stem + append_str).with_suffix(path_.suffix))


def replace_parent(path_, target_prarent):
    path_ = Path(path_)
    return str(Path(target_prarent) / path_.name)


def glob_dir(
    dir_,
    include_patterns: Union[List[str], None] = None,
    exclude_patterns: Union[List[str], None] = None,
    ignore_case=False,
) -> Iterator[Path]:
    """Glob directory recursively and filter paths by extensions and filename suffix

    Args:
        dir_: directory path
        include_patterns: list of include patterns, eg ["*.png", "*.txt"]
        exclude_patterns: list of exclude patterns, eg: ["*mask.png", "*mask.txt"]
        ignore_case: case sensitive match or not

    Returns:
        Iterator[Path]: an iterator of matched paths under given directory

    Raises:
        FileNotFoundError: If given directory dose not exist

    Examples:
    # glob current directory, get .py files without *version.py like files
    >>> glob_dir(".", include_patterns=["*.py"], exclude_patterns=["*version.py"])
    """
    dir_ = Path(dir_)

    if not dir_.is_dir():
        raise FileNotFoundError(f"directory {dir_} dose not exist!")

    def all_pass_filter(_):
        return True

    def _include_filter(p: Path):
        if ignore_case:
            p = Path(p.as_posix().lower())

        return any(p.match(pattern) for pattern in include_patterns)  # type: ignore

    def _exclude_filter(p: Path):
        if ignore_case:
            p = Path(p.as_posix().lower())

        return all(not p.match(pattern) for pattern in exclude_patterns)  # type: ignore

    include_filter = _include_filter if include_patterns else all_pass_filter
    exclude_filter = _exclude_filter if exclude_patterns else all_pass_filter

    def path_filter(path: Path):
        return include_filter(path) and exclude_filter(path)

    return filter(path_filter, dir_.rglob("*"))


def load_xml(filename):
    return ET.parse(str(filename))


def dump_xml(filename, method="r", encoding="utf-8"):
    pass


def load_yaml(filename, method="r", encoding="utf-8"):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    if "b" in method:
        with open(filename, method) as f:
            return yaml.load(stream=f, Loader=yaml.FullLoader)
    else:
        with open(filename, method, encoding=encoding) as f:
            return yaml.load(stream=f, Loader=yaml.FullLoader)


def dump_yaml(data, filename, method="w", encoding="utf-8", safe_mode=False, **kwargs):
    """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.
    """
    if safe_mode:
        temp_file_name = filename + "_temp"
    else:
        temp_file_name = filename

    with open(temp_file_name, method) as f:
        if "b" in method:
            ret = yaml.dump(data=data, stream=f, encoding=encoding, **kwargs)
        else:
            ret = yaml.dump(data=data, stream=f, **kwargs)
        if safe_mode:
            f.flush()
            os.fsync(f.fileno())

    if safe_mode:
        os.rename(temp_file_name, filename)

    return ret


def load_json(filename, method="r", **kwargs):
    if method == "r":
        with open(filename, method) as f:
            data = json.load(f, **kwargs)
    elif method == "rb":
        decode_method = kwargs.get("encoding", None)
        with open(filename, method) as f:
            data = f.read()
            if decode_method is not None:
                data = data.decode(decode_method)
                data = json.loads(data)
    return data


def dump_json(data, filename, method="w", indent=None, safe_mode=False, **kwargs):
    """
    Dump data to json file

    Args:
        data: json serializable python object, dict, list etc...
            dumped data
        filename: str or Path
            path of dumped json file
        method(str): an optional string that specifies the mode in which the file
            is opened
        indent: None or int
            If ``indent`` is a non-negative integer, then JSON array elements and
            object members will be pretty-printed with that indent level. An indent
            level of 0 will only insert newlines. ``None`` is the most compact
            representation.
        safe_mode(bool): Dump in safe mode or not
    """
    if safe_mode:
        temp_file_name = filename + "_temp"
    else:
        temp_file_name = filename

    if "b" in method:
        raise ValueError("can not dump json with binary mode!")

    with open(temp_file_name, method) as f:
        json.dump(obj=data, fp=f, indent=indent, **kwargs)

        if safe_mode:
            f.flush()
            os.fsync(f.fileno())

    if safe_mode:
        os.rename(temp_file_name, filename)


def copy_related_files(
    src_dir,
    dst_dir,
    ref_dir,
    copy=True,
    src_suffix=None,
    ref_suffix=None,
    parents=True,
    exist_ok=True,
):
    src_dir = Path(src_dir).absolute()
    dst_dir = Path(dst_dir).absolute()
    ref_dir = Path(ref_dir).absolute()
    Path(str(ref_dir)).mkdir(parents=parents, exist_ok=exist_ok)
    ref_file_list = list(
        glob_dir(
            ref_dir,
            include_patterns=[f"*{ref_suffix}"] if ref_suffix is not None else None,
        )
    )
    for ref_file_path in ref_file_list:

        ref_file_name = ref_file_path.name
        if ref_suffix is not None:
            src_file_name = ref_file_name.split(ref_suffix)[0]
        else:
            src_file_name = ref_file_name
        if src_suffix is not None:
            src_file_name += src_suffix
        src_file_path = Path(src_dir) / src_file_name

        if not Path(src_file_path).exists():
            logger.warning(f"{src_file_path} does not exist.")
        elif copy:
            shutil.copy(src_file_path, Path(dst_dir) / src_file_name)
        else:
            shutil.move(src_file_path, Path(dst_dir) / src_file_name)
