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
    def create_tasks(names : List[str], base_dir : str, resource_groups : Dict[ResourceType, ResourceGroup]) -> None:
        unique_names = TaskFactory.get_task_dependencies(names)
        unique_names = list(set(names))

        for name in unique_names:
            # Capitalize first character of string
            name = name[0].upper() + name[1:]
            cls = TaskFactory._tasks[name]
            assert cls is not None
            output_dir = os.path.join(base_dir, cls.__name__.lower())

            # Create resource groups for algorithm
            required_resources = cls.get_input_types()
            for each_resource in required_resources:
                resource_groups[each_resource] = ResourceGroup(each_resource)

            print(f'Inside task factory creating { cls.__name__ } {output_dir} and {resource_groups}')

            cls(output_dir, resource_groups) #TODO pass in output_dir


    @staticmethod
    def get_task_dependencies(names: List[str]) -> List[str]:
        all_names = names

        for i in range(len(names)):
            name = names[i]
            # Capitalize first character of string
            name = name[0].upper() + name[1:]
            cls = TaskFactory._tasks[name]
            assert cls is not None
            req_inputs = cls.get_input_types()
            print(f'{cls.__name__} has inputs {req_inputs}')
            depends = TaskFactory.get_tasks_with_outputs(req_inputs)

            all_names += depends


    @staticmethod
    def get_tasks_with_outputs(resource_types : List[ResourceType]) -> List[ResourceType]:
        output = []

        if resource_types is not None:
            for type in resource_types:
                for task in TaskFactory._tasks:
                    cls = TaskFactory._tasks[task]

                    if cls.get_output_types() is None:
                        continue

                    if type in cls.get_output_types():
                        print(f'{cls.__name__} has outputs {type}')
                        output.append(cls.get_name())

        return list(set(output))


class Task(ABC, metaclass=TaskMetaclass):
    """Class to manage an algorithm."""
    ###__metaclass__= TaskMetaclass

    def __init__(self, output_dir : str, resource_dict : Dict[ResourceType, ResourceGroup], execution_data: Dict[str, str]={}) -> None:
        super().__init__()
        self.output_dir = output_dir
        self.execution_data = execution_data
        self.resource_dict = resource_dict

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


    @abstractmethod
    def run(self) -> Dict[str, str]:
        """Execute Task"""
        pass


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
    
    def get_output_zip(self) -> str:
        """Zips output directory and returns zip path"""
        #TODO: Implement Method
        pass

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
