#!/usr/bin/env python3

import sys
import re
import unittest
from unittest.mock import Mock
from catrename.NamePart import NamePart


class TestNamePart(unittest.TestCase):

    def setUp(self):
        self.part_pattern = Mock()
        self.part_pattern.name = 'all'
        self.part_pattern.regex = re.compile('.*')
        self.part_pattern.transformation = lambda x: x.replace('a', 'b')
        self.namepart = NamePart(self.part_pattern, 'aaaaa')

    def test_init(self):
        self.assertEqual(self.namepart.part_pattern, self.part_pattern)
        self.assertEqual(self.namepart.name_part, 'aaaaa')
        self.assertFalse(self.namepart.transformed)

    def test_transform(self):
        self.namepart.transform()
        self.assertEqual(self.namepart.name_part, 'bbbbb')
        self.assertTrue(self.namepart.transformed)

    def test_get_name(self):
        self.assertEqual(self.namepart.get_name(), self.namepart.part_pattern.name)

if __name__ == "__main__":
    unittest.main(buffer=True)
