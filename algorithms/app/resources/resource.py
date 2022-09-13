from typing import TypeVar, Generic, List, Callable
from wsgiref.validate import validator
from resources.resource_types import ResourceType

T = TypeVar('T')

class ResourceWrapper(Generic[T]):

    def __init__(self, path : str, origin : str, metadata : T = None):
        self._path = path
        self._origin = origin
        self._metadata = metadata


class ResourceGroup(Generic[T]):

    def __init__(self, type: ResourceType, validate : Callable[[List[ResourceWrapper[T]], ResourceWrapper[T]], bool]):
        self._type = type
        self._validator = validate

        self._resources = []
        self._subscribers = []
        self._providers = {}


    def is_active(self) -> bool:
        done = True

        for (_, completed) in self._providers:
            done = done and completed

        return not done

    def get_all_resources(self) -> List[ResourceWrapper[T]]:
        return self._resources
    
    
    def subscribe(self, callback : Callable[[ResourceWrapper[T]], bool]) -> None:
        """Adds new subscriber to list"""
        self._subscribers.append(callback)


    def dispatch(self, resource : ResourceWrapper[T], completed : bool) -> None:
        """Adds new resource to resources list and notifies all subscribers"""
        if not self._validator(self._resources, resource):
            return
        
        self._providers[resource.origin] = completed
        self._resources.append(resource)

        ## TODO store dispatched resources in JSON or something and not just memory

        for callback in self._subscribers:
            self._active = self._active and callback(resource)
