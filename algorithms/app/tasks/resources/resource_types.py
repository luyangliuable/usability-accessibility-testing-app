from enum import Enum

class ResourceType(Enum):
    APK_FILE = 0,
    SCREENSHOT_PNG = 1,
    SCREENSHOT_JPEG = 2,
    XML_LAYOUT = 3,
    JSON_LAYOUT = 4,
    ACCESSABILITY_ISSUE = 5,
    DISPLAY_ISSUE = 6,
    TAPPABILITY_PREDICT = 7,
    UTG = 8,
    GIF = 9,
    ZIPS = 10,
    EMULATOR = 11,

