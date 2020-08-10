#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from catrename.RenamingSimulator import RenamingSimulator


class TestRenamingSimulator(unittest.TestCase):

    def setUp(self):
        self.rs = RenamingSimulator()
        self.category = Mock()
        self.file1 = Mock(dirname='/path', basename='old_name1.txt',
                          rename_to=Mock())
        self.file2 = Mock(dirname='/path/to', basename='old_name2.txt',
                          rename_to=Mock())
        self.category.files = [self.file1, self.file2]
        self.new_names = ['new_name1.txt', 'new_name2.txt']
        self.category.new_file_name.side_effect = self.new_names

    @patch('catrename.RenamingSimulator.print')
    def test_run(self, mock_print):
        self.rs.run(self.category)
        self.assertEqual(len(self.category.new_file_name.call_args_list),
                         len(self.category.files))
        self.file1.rename_to.assert_not_called()
        self.file2.rename_to.assert_not_called()
        self.assertEqual(len(mock_print.call_args_list),
                         len(self.category.files))


if __name__ == "__main__":
    unittest.main(buffer=False)
