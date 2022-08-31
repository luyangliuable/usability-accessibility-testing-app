from enum import Enum

class StatusEnum(str, Enum):
    running = "RUNNING"
    stopped = "STOPPED"
    failed = "FAILED"
    successful = "SUCCESSFUL"
