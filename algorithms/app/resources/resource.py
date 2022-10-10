from numbers import Number
from threading import Thread
from typing import TypeVar, Generic, List, Callable, Dict
from wsgiref.validate import validator
from resources.resource_types import ResourceType, ResourceUsage

T = TypeVar('T')    ## Metadata type

class ResourceWrapper(Generic[T]):
    """
    Wraps and manages a singular resource
    """

    def __init__(self, path : str, origin : str, metadata : T = None):
        self._path = path
        self._origin = origin
        self._metadata = metadata
        self._released = None

    def update_path(self, path: str) -> None:
        self._path = path

    def get_path(self) -> str:
        return self._path

    def get_origin(self) -> str:
        return self._origin

    def get_metadata(self) -> T:
        return self._metadata

    def set_metadata(self, metadata : T):
        self._metadata = metadata


    def __repr__(self):
        return f'<<{type( self ).__name__} path={self._path} released={self._released}>>'



    def lock(self, released):
        """
        Enforce a lock on the resource, providing an ON RELEASED callback
        """
        assert self._released is None
        self._released = released

    def release(self) -> None:
        """
        Release the lock on the resource, calling the ON RELEASED callback if it exists
        """
        callback = self._released
        self._released = None

        if callback is not None:
            callback(self)



class ResourceGroup(Generic[T]):
    """
    Keeps track of a specific type of resource, containing all the singular resources of that
    type within itself. Manages the publishing and subscribing to a resource type
    """

    def __init__(self, type: ResourceType, usage: ResourceUsage = ResourceUsage.CONCURRENT):
        self._type = type
        self._resources = []
        self._subscribers = []
        self._providers = {}
        self._usage = usage


    def is_active(self) -> bool:
        ## TODO rework active status of resource group
        done = True

        for (_, completed) in self._providers:
            done = done and completed

        return not done


    def subscribe(self, callback : Callable[[ResourceWrapper[T]], None]) -> None:
        """
        Subscribe to the resource group
        """
        print('Droidbot subscribed')
        self._subscribers.append(callback)


    def publish(self, resource : ResourceWrapper[T], completed : bool) -> None:
        """
        Add a resource to the group and notify all subscribers
        """
        self._providers[resource.get_origin()] = completed
        print(f'{resource} added to {self._resources}.')
        self._resources.append(resource)

        # TODO new utg class, callback for utg:
        # Has data whether the utg finished building.
        # TODO if the resource being publish is utg and with images from droidbot, ignore ones the same hash.

        # TODO if the resource being published is utg, run trigger run to utg.

        ## TODO store dispatched resources in JSON or something and not just memory
        if self._usage is ResourceUsage.CONCURRENT:
            for sub in self._subscribers:
                sub(resource)

        elif self._usage is ResourceUsage.SEQUENTIAL:
            self.lock_resource(resource, 0)


    def lock_resource(self, resource : ResourceWrapper[T], index : Number) -> None:
        """
        INTERNAL USE ONLY
        Place a sequential lock on a resource, allows a resource to be dispatches sequentially
        instead of concurrently
        """
        if index >= len(self._subscribers):
            return

        resource.lock(lambda x : self.lock_resource(x, index + 1))
        self._subscribers[index](resource)
 
