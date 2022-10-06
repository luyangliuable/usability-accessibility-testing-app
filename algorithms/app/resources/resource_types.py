from enum import Enum


class ResourceType(Enum):
    """
    Defines different groups for resources to be published to
    """
    
    EMULATOR = 0
    APK_FILE = 1
    SCREENSHOT = 2
    UTG = 3
    GIF = 4
    ACCESSIBILITY_ISSUE = 5
    DISPLAY_ISSUE = 6
    TAPPABILITY_PREDICTION = 7
    
    

    
class ResourceUsage(Enum):
    """
    Defines how a resource group will dispatch a resource.

    CONCURRENT means the resource group will give the resource to all subscribers at the same time

    SEQUENTIAL means the resource group will give the resource to one subscriber at a time, waiting
        for it to finish using it before moving onto the next subscriber (i.e. Emulator resource)
    """
    CONCURRENT = 0,
    SEQUENTIAL = 1,