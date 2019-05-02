from pathlib import Path


class Cut:
    def __init__(self, input_dir, output_dir, size, internal=True):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.size = size
        self.internal = internal

    def load_materials(self):
        Path(self.input_dir).glob('*.json')

