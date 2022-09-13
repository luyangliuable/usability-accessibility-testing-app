from enum import Enum

class ResourceType(Enum):
    APK_FILE = 0,
    SCREENSHOT_PNG = 1,
    SCREENSHOT_JPEG = 2,
    SCREENSHOT_UNIQUE = 3,
    XML_LAYOUT = 4,
    JSON_LAYOUT = 5,
    ACCESSABILITY_ISSUE = 6,
    DISPLAY_ISSUE = 7,
    TAPPABILITY_PREDICT = 8,
    UTG = 9,
    GIF = 10,
    ZIPS = 11,

