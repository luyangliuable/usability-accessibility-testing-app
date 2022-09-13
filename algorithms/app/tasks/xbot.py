from tasks.task import Task
import os

class Xbot(Task):
    """Class for managing Xbot algorithm"""
    
    def __init__(self, resource_groups) -> None:
        super().__init__(output_dir, "xbot")
        self.apk_path = apk_path
        self.emulator = emulator    ## TODO


    def execute(self) -> None:
        data = {
            "apk_path":self.apk_path,
            "output_dir":self.output_dir,
            "emulator": self.emulator
        }
        response = self.http_request(url=self.url, data=data)
        
        self.status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'