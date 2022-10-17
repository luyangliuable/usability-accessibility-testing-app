from resources.resource import ResourceWrapper
from resources.singleton_meta import SingletonMeta

class Emulator(ResourceWrapper, SingletonMeta ):
    """
    Wraps and manages a singular resource
    """
    def __init__(self, path : str, origin : str, metadata : T = None):
        super().__init__(path, origin, metadata)

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
        return f'<<Resource Wrapper path={self._path}, released={self._released}, origin={self._origin}, metadata={self._metadata.__class__.__name__}>>'


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
