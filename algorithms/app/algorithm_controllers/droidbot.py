from algorithm_controllers.task import Task
import os

class Droidbot(Task):
    """Class for managing droidbot algorithm"""
    
    def __init__(self, apk_path, output_dir, emulator) -> None:
        self.apk_path = apk_path
        self.emulator = emulator
        super().__init__(output_dir, "droidbot", None)

    def execute(self) -> None:
        # TODO: implement method
        pass