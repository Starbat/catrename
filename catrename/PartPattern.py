import re


class PartPattern:

    def __init__(self, name, regex, transformation=lambda x: x):
        self.name = name
        self.regex = re.compile(regex)
        self.transformation = transformation
