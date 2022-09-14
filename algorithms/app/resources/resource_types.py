from enum import Enum


class ResourceType(Enum):
    """
    Defines different groups for resources to be published to
    """
    APK_FILE = 0,
    SCREENSHOT_PNG = 1,
    SCREENSHOT_JPEG = 2,
    SCREENSHOT_UNIQUEPAIR = 3,
    XML_LAYOUT = 4,
    JSON_LAYOUT = 5,
    ACCESSABILITY_ISSUE = 6,
    DISPLAY_ISSUE = 7,
    TAPPABILITY_PREDICT = 8,
    UTG = 9,
    GIF = 10,
    ZIPS = 11,
    EMULATOR = 12,


class ResourceUsage(Enum):
    """
    Defines how a resource group will dispatch a resource.

    CONCURRENT means the resource group will give the resource to all subscribers at the same time

    SEQUENTIAL means the resource group will give the resource to one subscriber at a time, waiting
        for it to finish using it before moving onto the next subscriber (i.e. Emulator resource)
    """
    CONCURRENT = 0,
    SEQUENTIAL = 1,