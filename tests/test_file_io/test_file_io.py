# -*- coding:utf-8 -*-
# @FileName :test_file_io.py
# @Author   :Deyu He
# @Time     :2022/12/16 10:27

from pathlib import Path
from unittest import TestCase

from pyutils.file_io.core import copy_related_files, replace_parent


class TestFileIO(TestCase):
    def test_copy_related_files(self):
        src_dir = r"../test_data/src_files"
        ref_dir = r"../test_data/ref_files"
        dst_dir = r"../test_data/dst_files"
        copy_related_files(
            src_dir, dst_dir, ref_dir, src_suffix="_input.bmp", ref_suffix="_output.bmp"
        )

    def test_replace_parent(self):
        path_ = r"C:/test/x.bmp"
        target_parent = r"D:/1"
        assert replace_parent(path_, target_parent) == str(
            Path(r"D:/1/x.bmp").absolute()
        )
