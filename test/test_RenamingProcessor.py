#!/usr/bin/env python3

import sys
import unittest
from os.path import basename, dirname, join
from unittest.mock import patch, Mock
from catrename.RenamingProcessor import RenamingProcessor


class TestRenamingProcessor(unittest.TestCase):

    def setUp(self):
        self.rp = RenamingProcessor()
        self.category = Mock()
        self.old_names = ['old_name1.txt', 'old_name2.txt']
        self.file1 = Mock(dirname='/path', basename=self.old_names[0],
                     rename_to=Mock(return_value=True))
        self.file2 = Mock(dirname='/path/to', basename=self.old_names[1],
                     rename_to=Mock(return_value=True))
        self.category.files = [self.file1, self.file2]
        self.new_names = ['new_name1.txt', 'new_name2.txt']
        self.category.new_file_name.side_effect = self.new_names

    @patch('catrename.RenamingProcessor.print')
    @patch('catrename.RenamingProcessor.sys.stderr')
    def test_run(self, mock_stderr, mock_print):
        self.rp.run(self.category)
        self.assertEqual(len(self.category.new_file_name.call_args_list),
                         len(self.category.files))
        self.file1.rename_to.assert_called_with(self.new_names[0])
        self.file2.rename_to.assert_called_with(self.new_names[1])
        self.assertEqual(len(mock_print.call_args_list),
                         len(self.category.files))

        self.setUp()
        mock_print.reset_mock()
        self.file1.rename_to=Mock(return_value=False)
        self.file2.rename_to=Mock(return_value=False)
        self.rp.run(self.category)
        self.assertEqual(len(mock_print.call_args_list),
                         len(self.category.files))

        # Do not rename files if the new name is identical to the old name.
        self.setUp()
        mock_print.reset_mock()
        self.category.new_file_name.side_effect = self.old_names
        self.rp.run(self.category)
        self.file1.rename_to.assert_not_called()
        self.file2.rename_to.assert_not_called()
        self.assertEqual(len(mock_print.call_args_list),
                         len(self.category.files))


if __name__ == "__main__":
    unittest.main(buffer=True)
