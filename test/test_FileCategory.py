#!/usr/bin/env python3

import re
import unittest
from unittest.mock import Mock, MagicMock
from string import Template
from catrename.FileCategory import FileCategory


class TestFileCategory(unittest.TestCase):

    def setUp(self):
        part_pattern = Mock()
        part_pattern.name = 'all'
        part_pattern.regex = re.compile('.*')
        part_pattern.transformation = lambda x: x
        self.fc = FileCategory('great category', '1.*', [part_pattern],
                               '${all}')
        self.file1 = MagicMock(dirname='/path/to', basename='1_file.txt')
        self.file2 = MagicMock(dirname='/path/to', basename='2_file.txt')

    def test_init(self):
        self.assertIsInstance(self.fc.IDENTIFIER, re.Pattern)
        self.assertIsInstance(self.fc.TEMPLATE, Template)

    def test_add_file(self):
        val = self.fc.add_file(self.file1)
        self.assertTrue(val, 'Matching files will be added.')
        self.assertEqual(len(self.fc.files), 1)

        val = self.fc.add_file(self.file2)
        self.assertFalse(val, 'Not matching files will not be added.')
        self.assertEqual(len(self.fc.files), 1)

    def test_new_file_name(self):
        file = Mock()
        file.find_name_parts = Mock()
        file.transform_parts = Mock()
        file.get_part_dict = Mock(return_value={'a': 1, 'b': 2})
        self.fc.TEMPLATE.substitute = Mock()
        self.fc.POSTPROC = Mock()
        _ = self.fc.new_file_name(file)

        self.assertTrue(file.find_name_parts.called)
        self.assertTrue(file.transform_parts.called)
        self.assertTrue(self.fc.TEMPLATE.substitute.called)
        self.assertTrue(self.fc.POSTPROC.called)

    def test_str(self):
        output = str(self.fc)

        name = self.fc.NAME
        identifier = str(self.fc.IDENTIFIER)
        part_patterns = self.fc.PART_PATTERNS
        template = self.fc.TEMPLATE
        postproc = self.fc.POSTPROC
        files = self.fc.files
        expected = (f'NAME: {name}, IDENTIFIER: {identifier}, ' +
                    f'PART_PATTERNS: {part_patterns}, ' +
                    f'TEMPLATE: {template}, POSTPROC: {postproc}, ' +
                    f'files: {files}')

        self.assertEqual(type(output), str)
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main(buffer=True)
