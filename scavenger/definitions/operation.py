from enum import auto, Enum, unique
from rx.subjects import Subject
from scavenger.

class Operation(Subject):
	@unique
	class Category(Enum):
		START	= auto()

__all__ = [
	'Operation'
]