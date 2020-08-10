#!/usr/bin/env python3

import re
import unittest
from catrename.PartPattern import PartPattern


class TestPartPattern(unittest.TestCase):

    def setUp(self):
        name = 'pattern'
        regex = '.*'
        self.part_pattern = PartPattern(name, regex)

    def test_init(self):
        self.assertEqual(self.part_pattern.name, 'pattern')
        self.assertEqual(type(self.part_pattern.regex), re.Pattern)
        self.assertTrue(callable(self.part_pattern.transformation))


if __name__ == "__main__":
    unittest.main(buffer=True)
