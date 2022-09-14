from numbers import Number
from threading import Thread
from typing import TypeVar, Generic, List, Callable, Dict
from wsgiref.validate import validator
from resources.resource_types import ResourceType, ResourceUsage

T = TypeVar('T')    ## Metadata type

class ResourceWrapper(Generic[T]):
    """Class to manage a single APK resource"""

    def __init__(self, path : str, origin : str, metadata : T = None):
        self._path = path
        self._origin = origin
        self._metadata = metadata

        self._released = None

    def get_path(self) -> str:
        return self._path
    
    def get_origin(self) -> str:
        return self._origin
    
    def get_metadata(self) -> T:
        return self._metadata

    def set_metadata(self, metadata : T):
        self._metadata = metadata
    
    

    def lock(self, released):
        assert self._released is None
        self._released = released

    def release(self) -> None:
        callback = self._released
        self._released = None

        if callback is not None:
            callback(self)



class ResourceGroup(Generic[T]):

    def __init__(self, type: ResourceType, usage: ResourceUsage = ResourceUsage.CONCURRENT):
        self._type = type

        self._resources = []
        self._subscribers = []
        self._providers = {}
        self._usage = usage

    def is_active(self) -> bool:
        done = True

        for (_, completed) in self._providers:
            done = done and completed

        return not done

    def get_all_resources(self) -> List[ResourceWrapper[T]]:
        """get list of resources"""
        return self._resources
    
    
    def subscribe(self, callback : Callable[[ResourceWrapper[T]], None]) -> None:
        """Adds new subscriber to list"""
        self._subscribers.append(callback)

    
    def reg_provider(self, origin : str) -> None:
        self._providers[origin] = False


    def publish(self, resource : ResourceWrapper[T], completed : bool) -> None:
        """Adds new resource to resources list and notifies all subscribers"""
        
        self._providers[resource.get_origin()] = completed
        self._resources.append(resource)


        ## TODO store dispatched resources in JSON or something and not just memory


        if self._usage is ResourceUsage.CONCURRENT:
            for sub in self._subscribers:
                sub(resource)


        elif self._usage is ResourceUsage.SEQUENTIAL:
            self.lock_resource(resource, 0)
            


    def lock_resource(self, resource : ResourceWrapper[T], index : Number) -> None:
        if index >= len(self._subscribers):
            return

        resource.lock(lambda x : self.lock_resource(x, index + 1))
        self._subscribers[index](resource)