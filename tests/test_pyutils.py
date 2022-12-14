#!/usr/bin/env python

"""Tests for `pyutils` package."""

from pyutils.pyutils import sample


def test_sample():
    assert sample(True)
    assert not sample(False)
