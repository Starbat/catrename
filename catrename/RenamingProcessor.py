import os
import sys


class RenamingProcessor:

    def run(self, category):
        for file in category.files:
            new_name = category.new_file_name(file)
            if new_name is not file.basename:
                old_path = os.path.join(file.dirname, file.basename)
                new_path = os.path.join(file.dirname, new_name)
                success = file.rename_to(new_name)
                if success:
                    print(f'{old_path} -> {new_path}')
                else:
                    print(f'{old_path}: error during renaming.',
                          file=sys.stderr)
            else:
                print(f'{file} was not changed.', file=sys.stderr)
