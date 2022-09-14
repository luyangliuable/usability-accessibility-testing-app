from typing import TypeVar, Generic, List, Callable, Dict
from wsgiref.validate import validator
from resources.resource_types import ResourceType

T = TypeVar('T')

class ResourceWrapper(Generic[T]):
    """Class to manage a single APK resource"""

    def __init__(self, path : str, origin : str, metadata : T = None):
        self._path = path
        self._origin = origin
        self._metadata = metadata

    def get_path(self) -> str:
        return self._path
    
    def get_origin(self) -> str:
        return self._origin
    
    def get_metadata(self) -> T:
        return self._metadata

    def set_metadata(self, metadata):
        self._metadata = metadata


class ResourceGroup(Generic[T]):

    def __init__(self, type: ResourceType):
        self._type = type

        self._resources = []
        self._subscribers = []
        self._providers = {}

    def is_active(self) -> bool:
        done = True

        for (_, completed) in self._providers:
            done = done and completed

        return not done

    def get_all_resources(self) -> List[ResourceWrapper[T]]:
        """get list of resources"""
        return self._resources
    
    
    def subscribe(self, callback : Callable[[ResourceWrapper[T]], bool]) -> None:
        """Adds new subscriber to list"""
        self._subscribers.append(callback)
    
    def reg_provider(self, origin : str) -> None:
        self._providers[origin] = False


    def dispatch(self, resource : ResourceWrapper[T], completed : bool) -> None:
        """Adds new resource to resources list and notifies all subscribers"""
        
        self._providers[resource.get_origin()] = completed
        self._resources.append(resource)

        ## TODO store dispatched resources in JSON or something and not just memory

        for callback in self._subscribers:
            callback(resource)