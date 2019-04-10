from enum import auto, Enum, unique
from scavenger.api.definitions import mixins

@unique
class Status(mixins.EnumParser, Enum):
    INITIATING	= auto()
    RUNNING		= auto()
    SHUTTING	= auto()
    TERMINATING	= auto()
    FAILED		= auto()
    TERMINATED	= auto()
    COMPLETED	= auto()