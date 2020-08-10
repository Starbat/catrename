import sys
import re
from .FileCategory import FileCategory
from .PartPattern import PartPattern


class FileProcessor:

    def __init__(self, rules, process):
        self.CATEGORIES = self._create_categories(rules)
        self.PROCESS = process

    def _create_categories(self, rules):
        categories = []
        for category, probs in rules.items():
            part_patterns = self._create_part_patterns(probs['parts'])
            args = [category, probs['identifier'],
                    part_patterns, probs['template']]
            if 'postproc' in probs:
                args.append(probs['postproc'])
            categories.append(FileCategory(*args))
        return categories

    def _create_part_patterns(self, parts):
        part_patterns = []
        for part, probs in parts.items():
            args = [part, probs['regex']]
            if 'transform' in probs:
                args.append(probs['transform'])
            part_patterns.append(PartPattern(*args))
        return part_patterns

    def get_category(self, file):
        matches = [c for c in self.CATEGORIES
                   if re.match(c.IDENTIFIER, file.basename)]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) < 1:
            print(f'{file} matches no identifier.', file=sys.stderr)
        else:
            print(f'{file} matches multiple identifiers.',
                  file=sys.stderr)
        return None

    def add_files(self, *files):
        for file in files:
            category = self.get_category(file)
            if category:
                category.add_file(file)

    def run(self):
        for c in self.CATEGORIES:
            self.PROCESS.run(c)
