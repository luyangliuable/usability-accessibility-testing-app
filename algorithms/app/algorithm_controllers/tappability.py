from algorithm_controllers.task import Task
import os

class Tappability(Task):
    """Class for managing Tappability algorithm"""
    
    def __init__(self, image_dir, layout_dir, output_dir) -> None:
        self.image_dir = image_dir
        self.layout_dir = layout_dir
        super().__init__(output_dir, "tappable", None)

    def execute(self) -> None:
        data = {
            "image_dir" : self.image_dir,
            "layout_dir" : self.layout_dir,
            "output_dir" : self.output_dir
        }
        response = self.http_request(url=self.url, data=data)
        
        self.status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'