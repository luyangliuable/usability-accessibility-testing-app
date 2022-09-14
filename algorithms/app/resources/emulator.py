from typing import List, Callable







class Emulator:
    """
    REDUNDANT
    
    Class to manage queue for using emulators emulators
    
    When a task requires an emulator it can subscribe to a queue and provide a callback 
    When the emulator is available it will notify next subscriber with the emulator name 
    """
    
    def __init__(self, name) -> None:
        self.name = name
        self.is_free = True
        self.subscribers = []
        
    def get_name(self) -> str:
        return self.name
    
    def subscribe(self, subscriber : Callable[[str],None]) -> None:
        """Subscriber for emulator"""
        self.subscribers.append(subscriber) # add subscriber to queue
        self._update_queue()
        
    
    def free_emulator(self) -> None:
        """Called when a subscriber is finished with the emulator"""
        self.in_use = False
        self._update_queue()
        
        
    def _update_queue(self) -> None:
        """Notifies next subscriber if emulator is free"""
        # if there are more subscribers and emulator is free, notify the next
        if len(self.subscribers) > 0 and self.is_free:  
            self.subscribers.pop(0)(self.name)
            self.is_free = False
            
        
        
        