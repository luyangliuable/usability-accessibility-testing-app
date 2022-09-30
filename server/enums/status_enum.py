from enum import Enum

class StatusEnum(str, Enum):
    none = "NOT_STARTED"
    running = "RUNNING"
    stopped = "STOPPED"
    failed = "FAILED"
    successful = "SUCCESSFUL"
