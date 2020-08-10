#!/usr/bin/env python3

import sys
import os
import yaml
from .File import File
from .RenamingProcessor import RenamingProcessor
from .RenamingSimulator import RenamingSimulator
from .FileProcessor import FileProcessor


class Renamer:

    def __init__(self, config, paths, recursive=False, simulate=False):
        rules = self.load_yaml(config)
        process = RenamingSimulator() if simulate else RenamingProcessor()
        self.file_processor = FileProcessor(rules, process)

        self.files = self._get_files(paths, recursive)
        self.recursive = recursive

    def rename(self):
        self.file_processor.add_files(*self.files)
        self.file_processor.run()

    def _get_files(self, paths, recursive=False):
        file_list = []
        for path in paths:
            if os.path.isfile(path):
                file_list.append(File(path))
            elif os.path.isdir(path):
                if recursive:
                    for dir, _, files in os.walk(path):
                        for file in files:
                            f = File(os.path.join(dir, file))
                            file_list.append(f)
                else:
                    print(f'{path} is a directory. Use the -r flag to ' +
                          'search folders recursively.',
                          file=sys.stderr)
            else:
                print(f'{path} does not exist.', file=sys.stderr)
        return file_list

    def load_yaml(self, path):
        with open(path) as f:
            rules = yaml.load(f, Loader=yaml.FullLoader)
        return rules
