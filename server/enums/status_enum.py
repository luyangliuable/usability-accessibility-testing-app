from enum import Enum

class StatusEnum(str, Enum):
    running = "RUNNING"
    stopped = "STOPPED"
    done = "DONE"
