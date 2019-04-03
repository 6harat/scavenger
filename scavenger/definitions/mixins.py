from enum import Enum
from scavenger.definitions.commons import JsonSerializable_

class EnumParserMixin:
	@classmethod
	def all_names(cls):
		return list(map(lambda v: v.name, cls))
	
	@classmethod
	def parse(cls, value):
		if isinstance(value, Enum):
			return value if value in cls else None
		if isinstance(value, str):
			fmt_value = value.upper().strip()
			try: this_enum = cls(fmt_value)
			except: this_enum = None
			return this_enum

class EnumSerializerMixin(JsonSerializable_):
	def to_json(self):
		return self.name
	
	@classmethod
	def from_json(cls, data):
		return cls.parse(data)

__all__ = [
	'EnumParserMixin',
	'EnumSerializerMixin'
]