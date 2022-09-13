from tasks.task import Task
from resources import *
from typing import List
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