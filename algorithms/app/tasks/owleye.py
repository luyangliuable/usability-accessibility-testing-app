from tasks.task import Task
import os

class Owleye(Task):
    """Class for managing Owleye algorithm"""
    
    def __init__(self, image_dir, output_dir) -> None:
        super().__init__(output_dir, "owleye")
        self.image_dir = image_dir

    def execute(self) -> None:  
        data = {
            "image_dir":self.image_dir,
            "output_dir":self.output_dir
        }
        response = self.http_request(url=self.url, data=data)
        
        self.status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'