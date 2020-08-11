#!/usr/bin/env python3

import unittest
from unittest.mock import patch, call, Mock
from catrename.Renamer import Renamer


class TestRenamer(unittest.TestCase):

    @patch('catrename.Renamer.FileProcessor')
    @patch('catrename.Renamer.ConfigLoader')
    @patch('catrename.Renamer.Renamer._get_files')
    def setUp(self, mock_get_files, mock_config_loader, mock_file_processor):
        self.mock_get_files = mock_get_files
        self.config_loader_instance = Mock()
        self.mock_config_loader = mock_config_loader
        self.mock_config_loader.return_value = self.config_loader_instance
        self.mock_file_processor = mock_file_processor
        self.renamer = Renamer("/path/categories.yaml",
                               ['/path/file1.txt', '/path/file2.txt'])

    def test_init(self):
        self.mock_get_files.assert_called_once()
        self.mock_config_loader.assert_called_once()
        self.config_loader_instance.load_yaml.assert_called_once()
        self.mock_file_processor.assert_called_once()

    @patch('catrename.Renamer.os.walk')
    @patch('catrename.Renamer.print')
    @patch('catrename.Renamer.os.path.isfile')
    @patch('catrename.Renamer.os.path.isdir')
    @patch('catrename.Renamer.File')
    def test_get_files(self, mock_file, mock_isdir, mock_isfile, mock_print,
                       mock_oswalk):
        paths = ['/path/file1.txt', '/path/to/', '/path/to/fileA.txt',
                 '/path/to/fileB.txt']
        mock_oswalk.return_value = [('/path/to',
                                     (),
                                     ('fileA.txt', 'fileB.txt'))]

        mock_isdir.return_value = False
        mock_isfile.return_value = False
        files = self.renamer._get_files(paths)
        self.assertEqual(len(files), 0,
                         'Don\' create Files for not existing paths.')
        self.assertEqual(mock_print.call_count, len(paths),
                         'Print error for not existing paths.')

        mock_isdir.return_value = False
        mock_isfile.return_value = True
        files = self.renamer._get_files([paths[0]])
        self.assertEqual(len(files), 1)

        mock_file.reset_mock()
        mock_isdir.return_value = True
        mock_isfile.side_effect = [True, False]
        files = self.renamer._get_files(paths[0:2], recursive=True)
        expected_calls = [call(paths[0]), call(paths[2]), call(paths[3])]
        self.assertEqual(mock_file.call_args_list, expected_calls,
                         'Create File objects for explicitly specified ' +
                         'files and files in directories.')
        self.assertEqual(len(files), 3,
                         'Create File object for each filepath.')

    def test_rename(self):
        self.renamer.rename()
        self.renamer.file_processor.add_files.assert_called()
        self.renamer.file_processor.run.assert_called()


if __name__ == "__main__":
    unittest.main(buffer=True)
