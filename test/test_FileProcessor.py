#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
from catrename.FileProcessor import FileProcessor


class TestFileProcessor(unittest.TestCase):

    rules = {'categoryA': {
                'identifier': '.*catA.*',
                'parts': {
                    'year': {'regex': '.*_(\d{4})\d{4}.*'},
                    'month': {'regex': '.*_\d{4}(\d{2})\d{2}.*'},
                    'day': {'regex': '.*_\d{6}(\d{2}).*'},
                    'info': {'regex': '.*\d{8}_(.*)\..*'},
                    'extension': {'regex': '.*\.(\w+)$'}
                    },
                'template': '${year}-${month}-{day}_A_${info}.${extension}',
                'postproc': 'replace_whitespace_by_underscore'
                },
             'categoryB': {
                'identifier': '.*catB.*',
                'parts': {
                    'year': {'regex': '.*_(\d{4})\d{4}.*'},
                    'month': {'regex': '.*_\d{4}(\d{2})\d{2}.*'},
                    'day': {'regex': '.*_\d{6}(\d{2}).*'},
                    'info': {'regex': '.*\d{8}_(.*)\..*',
                             'transform': 'lambda s: x.replace("a", "b")'},
                    'extension': {'regex': '.*\.(\w+)$'}
                    },
                'template': '${year}-${month}-{day}_B_${info}.${extension}'
                }
             }

    @patch('catrename.FileProcessor.FileProcessor._create_categories')
    def setUp(self, mock_create_categories):
        return_value = [Mock(id=k, IDENTIFIER=v['identifier'])
                        for k, v in self.rules.items()]
        mock_create_categories.return_value = return_value
        self.fp = FileProcessor(self.rules, Mock())

    @patch('catrename.FileProcessor.FileProcessor._create_categories')
    def test_init(self, mock_create_categories):
        _ = FileProcessor(self.rules, Mock())
        mock_create_categories.assert_called_with(self.rules)

    @patch('catrename.FileProcessor.FileCategory')
    def test_create_categories(self, mock_fc):
        self.fp._create_part_patterns = Mock()
        categories = self.fp._create_categories(self.rules)

        self.assertEqual(type(categories), list)
        self.assertEqual(len(categories), len(self.rules),
                         'Return one object for each rule.')
        self.assertTrue(self.fp._create_part_patterns.called_times(
                            len(self.rules)),
                        'Call create_part_patterns for each rule.')
        self.assertTrue(mock_fc.called_times(len(self.rules)),
                        'Create FileCategory for each rule.')

        ruleA = self.rules['categoryA']
        mock_fc.assert_any_call('categoryA', ruleA['identifier'],
                                self.fp._create_part_patterns(ruleA['parts']),
                                ruleA['template'], ruleA['postproc'])

        ruleB = self.rules['categoryB']
        mock_fc.assert_any_call('categoryB', ruleB['identifier'],
                                self.fp._create_part_patterns(ruleB['parts']),
                                ruleB['template'])

    @patch('catrename.FileProcessor.PartPattern')
    def test_create_part_patterns(self, mock_pp):
        partsA = self.rules['categoryA']['parts']
        _ = self.fp._create_part_patterns(partsA)

        self.assertEqual(mock_pp.call_count, len(partsA),
                         'Create one PartPattern for each entry.')
        for part, probs in partsA.items():
            mock_pp.assert_any_call(part, probs['regex'])

        mock_pp.reset_mock()
        partsB = self.rules['categoryB']['parts']
        _ = self.fp._create_part_patterns(partsB)

        self.assertEqual(mock_pp.call_count, len(partsB))
        mock_pp.assert_any_call('info', partsB['info']['regex'],
                                partsB['info']['transform'])

    def test_get_category(self):
        fileA = Mock(basename='file_catA.txt')
        category = self.fp.get_category(fileA)
        self.assertEqual(category.id, 'categoryA',
                         ('Return matching category if only one category ' +
                          'matches.'))

        fileB = Mock(basename='file_catB.txt')
        category = self.fp.get_category(fileB)
        self.assertEqual(category.id, 'categoryB',
                         ('Return matching category if only one category ' +
                          'matches.'))

        fileC = Mock(basename='file_catC.txt')
        category = self.fp.get_category(fileC)
        self.assertEqual(type(category), type(None),
                         'Return None if no category matches.')

        fileAB = Mock(basename='file_catA_catB.txt')
        category = self.fp.get_category(fileAB)
        self.assertEqual(type(category), type(None),
                         'Return None if multiple categories match.')

    def test_add_files(self):
        file = 'file.txt'
        category = Mock()

        self.fp.get_category = Mock(return_value=category)
        self.fp.add_files(file)
        self.fp.get_category.assert_called_once_with(file)
        category.add_file.assert_called_once()

        self.fp.get_category.reset_mock()
        self.fp.get_category = Mock(return_value=None)
        self.fp.add_files(file)
        self.fp.get_category.assert_called_once_with(file)

    @patch('catrename.FileProcessor.FileCategory')
    def test_run(self, mock_fc):
        self.fp.run()
        expected_times = len(self.fp.CATEGORIES)
        run_times = len(self.fp.PROCESS.run.call_args_list)
        self.assertEqual(run_times, expected_times)


if __name__ == "__main__":
    unittest.main(buffer=True)
