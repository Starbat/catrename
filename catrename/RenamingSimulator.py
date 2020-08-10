import os


class RenamingSimulator:

    def run(self, category):
        for file in category.files:
            new_name = category.new_file_name(file)
            old_path = os.path.join(file.dirname, file.basename)
            new_path = os.path.join(file.dirname, new_name)
            print(f'{old_path} -> {new_path}')
