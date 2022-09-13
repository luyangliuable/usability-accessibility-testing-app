from tasks.task import Task
import os

class Storydistiller(Task):
    """Class for managing Storydistiller algorithm"""
    
    def __init__(self, apk_path, output_dir, emulator) -> None:
        super().__init__(output_dir, "storydistiller")
        self.apk_path = apk_path
        self.emulator = emulator
        
    def execute(self) -> None:
        data = {
            "apk_path":self.apk_path,
            "output_dir":self.output_dir,
            "emulator": self.emulator
        }
        response = self.http_request(url=self.url, data=data)
        
        self.status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'

