from .transformations import *


class NamePart:

    def __init__(self, part_pattern, name_part):
        self.part_pattern = part_pattern
        self.name_part = name_part
        self.transformed = False

    def transform(self):
        if self.transformed:
            return False
        else:
            tf = self.part_pattern.transformation
            if type(tf) is str:
                fun = eval(tf)
            else:
                fun = tf
            self.name_part = fun(self.name_part)
            self.transformed = True
            return True

    def get_name(self):
        return self.part_pattern.name
