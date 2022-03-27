from enum import Enum


class Status(str, Enum):
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
