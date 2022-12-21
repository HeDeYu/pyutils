from unittest import TestCase

from loguru import logger

from pyutils.iterators.core import get_shuffle, make_cyclic_iterator


class TestIterators(TestCase):
    def test_make_cyclic_iterator(self):
        a = range(5)
        count_max = 15
        count = 0
        for x in make_cyclic_iterator(list(a)):
            logger.debug(x)
            count += 1
            if count == count_max:
                break
        logger.info("================================")
        count = 0
        for x in make_cyclic_iterator(range(5)):
            logger.debug(x)
            count += 1
            if count == count_max:
                break
        logger.info("================================")
        a = ["a", "b", "c", "d", "e"]
        count = 0
        for x in make_cyclic_iterator(a):
            logger.debug(x)
            count += 1
            if count == count_max:
                break

    def test_get_shuffle(self):
        l_ = [1, 2, 3, 4, 5]
        for _ in range(5):
            ret = get_shuffle(l_)
            logger.info(ret)

        l_ = ["a", "b", "c", "d"]
        for _ in range(5):
            ret = get_shuffle(l_)
            logger.info(ret)
