import os
import sys
import re
from .NamePart import NamePart


class File:

    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError
        self.basename = os.path.basename(path)
        self.dirname = os.path.dirname(path)
        self.name_parts = []

    def rename_to(self, new_basename):
        old_path = os.path.join(self.dirname, self.basename)
        new_path = os.path.join(self.dirname, new_basename)
        try:
            os.rename(old_path, new_path)
            self.basename = new_basename
            return True
        except Exception:
            return False

    def find_name_parts(self, part_patterns):
        self.name_parts = []
        for part_pattern in part_patterns:
            match = re.match(part_pattern.regex, self.basename)
            if match:
                name_part = NamePart(part_pattern, match[1])
                self.name_parts.append(name_part)

    def transform_parts(self):
        for p in self.name_parts:
            p.transform()

    def get_part_dict(self):
        return {p.get_name(): p.name_part for p in self.name_parts}

    def __str__(self):
        return os.path.join(self.dirname, self.basename)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    def __hash__(self):
        return hash(str(self))
