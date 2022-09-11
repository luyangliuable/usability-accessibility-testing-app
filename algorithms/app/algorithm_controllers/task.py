from abc import ABC, abstractmethod
import os
import requests

class Task(ABC):
    """Class to manage an algorithm."""
    
    def __init__(self, output_dir, name, status=None) -> None:
        super().__init__()
        self.output_dir = output_dir
        self.name = name
        self.status = status
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
    @abstractmethod
    def execute(self) -> None:
        """Runs the algorithm, saving output to self.output_dir"""
        pass
    
    def get_name(self) -> str:
        return self.name
    
    def get_status(self) -> str:
        return self.status
    
    def get_output_dir(self, name=None) -> str:
        """Returns output directory if name is None otherwise returns subdirectory name"""
        return self.output_dir
    
    def http_request(self, url, body):
        """Makes a http request with url and body
        
        returns response body
        """
        response = None
        error = None
        
        try: 
            request = requests.Session()
            response = request.post(url, json=body)
            return response
        
        except Exception as e:
            error = str(e)
            print("ERROR ON REQUEST: " + error)
        
        return response
