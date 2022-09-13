from tasks.task import Task
import os

class Gifdroid(Task):
    """Class for managing gifdroid algorithm"""
    
    def __init__(self, gif_path, utg_path, output_dir) -> None:
        self.gif_path = gif_path
        self.utg_path = utg_path
        super().__init__(output_dir, "gifdroid", None)

    def execute(self) -> None:
        # TODO: implement method
        pass