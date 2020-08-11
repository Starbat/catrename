import re
import sys


class FileCategory():

    def __init__(self, name, identifier, part_patterns, template,
                 postproc=lambda s: s):
        self.NAME = name
        self.IDENTIFIER = identifier
        self.PART_PATTERNS = part_patterns
        self.TEMPLATE = template
        self.POSTPROC = postproc
        self.files = set()

    def add_file(self, file):
        if re.match(self.IDENTIFIER, file.basename):
            self.files.add(file)
            return True
        else:
            return False

    def new_file_name(self, file):
        file.find_name_parts(self.PART_PATTERNS)
        file.transform_parts()
        transformed_parts = file.get_part_dict()
        try:
            new_name = self.TEMPLATE.substitute(transformed_parts)
        except KeyError as err:
            print(f'{file}: an error occurred with name part {err}. ' +
                  f'File classified as {self.NAME}.', file=sys.stderr)
            return file.basename
        new_name = self.POSTPROC(new_name)
        return new_name


    def __str__(self):
        return (f'NAME: {self.NAME}, IDENTIFIER: {self.IDENTIFIER}, ' +
                f'PART_PATTERNS: {self.PART_PATTERNS}, ' +
                f'TEMPLATE: {self.TEMPLATE}, POSTPROC: {self.POSTPROC}, ' +
                f'files: {self.files}')
