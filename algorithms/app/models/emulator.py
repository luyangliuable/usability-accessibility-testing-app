from dataclasses import dataclass


@dataclass
class Emulator:
    """Metadata for an emulator
    
    Attributes:
        name:               The name of the emulator.
        connection_str:     String used to connect to emulator. Eg: emulator-5554 or localhost:5554.
        resolution:         Emulator resolution (height, width). Eg: (1920, 1080).
        tasks:              List of tasks emulator is configured to run with. Default None type indicates emulator is configured for all tasks.
    """
    
    name: str
    connection_str: str
    resolution: tuple[int, int]
    tasks: set = None 
    
    
    def can_use(self, task_name: str) -> bool:
        """Check if emulator configured to use with a task class."""
        return not self.tasks or task_name in self.tasks
    

