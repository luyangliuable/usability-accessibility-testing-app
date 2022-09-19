import stat
from venv import create
from abc import ABC, ABCMeta, abstractmethod
from atexit import register
import os
import requests
from typing import TypeVar, Generic, List, Callable, Dict


from resources.resource import *

class TaskMetaclass(ABCMeta):
    def __new__(meta, name, bases, attrs):
        cls = super().__new__(meta, name, bases, attrs)
        TaskFactory._tasks[cls.__name__] = cls
        return cls

class TaskFactory:
    _tasks = {}

    @staticmethod
    def create_tasks(names : List[str], base_dir : str, resource_groups : Dict[ResourceType, ResourceGroup]) -> None: #TODO add output_dir para
        all_names = names

        for name in names:
            cls = TaskFactory._tasks[name]
            assert cls is not None

            req_inputs = cls.get_input_types()
            depends = TaskFactory.get_tasks_with_outputs(req_inputs)

            all_names += depends
            

        unique_names = list(set(all_names))

        for name in unique_names:
            cls = TaskFactory._tasks[name]
            assert cls is not None

            output_dir = os.path.join(base_dir, "%s".format(name))
            cls(output_dir, resource_groups) #TODO pass in output_dir

    @staticmethod
    def get_tasks_with_outputs(resource_types : List[ResourceType]) -> List[str]:
        names = []

        for type in resource_types:
            for task in TaskFactory._tasks:
                cls = TaskFactory._tasks[task]
                
                if cls.get_output_types() is None:
                    continue

                if type in cls.get_output_types():
                    names.append(cls.get_name())

        return list(set(names))


class Task(ABC, metaclass=TaskMetaclass):
    """Class to manage an algorithm."""
    ###__metaclass__= TaskMetaclass
    
    def __init__(self, output_dir : str, resource_dict : Dict[ResourceType, ResourceGroup]) -> None:
        super().__init__()
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
           os.makedirs(self.output_dir)
        self.resource_dict = resource_dict
        

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return
    
    @classmethod
    @abstractmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return

    @classmethod
    @abstractmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return

    def get_output_dir(self) -> str:
        """Output directory of the task"""
        return self.output_dir

    @classmethod
    def http_request(cls, url, body):
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