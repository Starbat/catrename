#!/usr/bin/env python3

import sys
import unittest
from os.path import basename, dirname, join
from unittest.mock import patch, Mock
from catrename.File import File
# from TestManager import TestManager
#
#
# tm = TestManager.get_instance()
# # Import module from ../src
# sys.path.insert(1, tm.SRC_DIR)
# from File import File


class TestFile(unittest.TestCase):

    @patch('catrename.File.os.path.isfile')
    def setUp(self, mock_isfile):
        mock_isfile.return_value = True
        self.path = '/path/to/file.txt'
        self.file = File(self.path)

    def test_init(self):
        self.assertEqual(self.file.basename, basename(self.path))
        self.assertEqual(self.file.dirname, dirname(self.path))

        not_existing = '/path/to/nothing.txt'
        with self.assertRaises(FileNotFoundError):
            File(not_existing)

    @patch('catrename.File.os')
    def test_rename_to(self, mock_os):
        new_name = 'document.pdf'

        out = self.file.rename_to(new_name)
        self.assertTrue(out, 'Returns true if renaming succeeded.')
        self.assertEqual(self.file.basename, new_name)
        self.assertTrue(mock_os.rename.called)

        mock_os.rename.side_effect = RuntimeError('error')
        out = self.file.rename_to('///')
        self.assertFalse(out, 'Returns false if renaming failed.')

    @patch('catrename.File.NamePart')
    def test_find_name_parts(self, mock_namepart):
        part_pattern = Mock()
        part_pattern.name = 'name'
        part_pattern.regex = '.*(fi).*'
        part_pattern.transformation = lambda s: s.replace('f', 's')

        self.file.find_name_parts([part_pattern])
        self.assertIsInstance(self.file.name_parts, list)
        mock_namepart.assert_called_once_with(part_pattern, 'fi')

    def test_transform_parts(self):
        self.file.name_parts = [Mock(), Mock()]
        self.file.transform_parts()
        for m in self.file.name_parts:
            self.assertTrue(m.transform.called)

    def test_get_part_dict(self):
        name_part1 = Mock()
        name_part1.get_name = Mock(return_value='a')
        name_part1.name_part = 1
        name_part2 = Mock()
        name_part2.get_name = Mock(return_value='b')
        name_part2.name_part = 2
        self.file.name_parts = [name_part1, name_part2]

        out = self.file.get_part_dict()
        self.assertIsInstance(out, dict)
        self.assertEqual(out['a'], 1)
        self.assertEqual(out['b'], 2)

    def test_str(self):
        string = str(self.file)
        self.assertEqual(string, join(self.file.dirname, self.file.basename))

    @patch('catrename.File.os.path.isfile')
    def test_eq(self, mock_isfile):
        mock_isfile.return_value = True
        other = File(self.path)
        self.assertEqual(self.file, other)

        other = File('/path/to/another/file.txt')
        self.assertNotEqual(self.file, other)

    @patch('catrename.File.os.path.isfile')
    def test_lt(self, mock_isfile):
        mock_isfile.return_value = True
        this = File('/path/to/No1.txt')
        that = File('/path/to/No2.txt')
        self.assertLess(this, that)

    @patch('catrename.File.os.path.isfile')
    def test_le(self, mock_isfile):
        mock_isfile.return_value = True
        this = File('/path/to/No1.txt')
        that = File('/path/to/No2.txt')
        self.assertLess(this, that)
        self.assertEqual(this, this)

    @patch('catrename.File.os.path.isfile')
    def test_gt(self, mock_isfile):
        mock_isfile.return_value = True
        this = File('/path/to/No2.txt')
        that = File('/path/to/No1.txt')
        self.assertGreater(this, that)

    @patch('catrename.File.os.path.isfile')
    def test_ge(self, mock_isfile):
        mock_isfile.return_value = True
        this = File('/path/to/No2.txt')
        that = File('/path/to/No1.txt')
        self.assertGreater(this, that)
        self.assertEqual(this, this)

    @patch('catrename.File.os.path.isfile')
    def test_hash(self, mock_isfile):
        mock_isfile.return_value = True
        this = File('/path/to/No1.txt')
        same = File('/path/to/No1.txt')
        that = File('/path/to/No2.txt')
        self.assertTrue(type(hash(self.file)), int)
        self.assertNotEqual(hash(this), hash(that))
        self.assertEqual(hash(this), hash(same))

if __name__ == "__main__":
    unittest.main(buffer=True)
