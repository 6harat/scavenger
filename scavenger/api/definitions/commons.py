from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import timedelta
from enum import auto, Enum, unique
from scavenger.api import util
from typing import Union

import abc
import functools
import logging as log

class interfaces:
	class JsonSerializable_:
		"""
		Declares methods required to be implemented for json serialization of enums and custom classes.
		Note: The interface is compliant to method names used by `dataclass_json` decorator.
		"""
		@abc.abstractclassmethod
		def from_json(cls, data):
			raise NotImplementedError
		
		@abc.abstractmethod
		def to_json(self):
			raise NotImplementedError


class mixins:
	class EnumParser(interfaces.JsonSerializable_):
		"""
		Provides helper methods to aid enum validation and parsing.
		"""
		@classmethod
		@functools.lru_cache()
		def all_names(cls):
			return tuple(map(lambda v: v.name, cls))
		
		@classmethod
		def parse(cls, value:Union[str, 'EnumParser']) -> 'EnumParser':
			#pylint: disable=unsupported-membership-test,unsubscriptable-object
			if isinstance(value, Enum):
				return value if value in cls else None
			
			fmt_value = str(value).upper().strip()
			try: return cls[fmt_value]
			except: return None

		def to_json(self) -> str:
			#pylint: disable=no-member
			return self.name
		
		@classmethod
		def from_json(cls, data: str) -> 'EnumParser':
			return cls.parse(data)


class invariants:
	@unique
	class FlushMode(mixins.EnumParser, Enum):
		"""
		Indicates flush strategy to be used by the manager.
		"""
		@dataclass_json
		@dataclass(frozen=True)
		class Params:
			num_record_limit	:int
			time_span_limit		:timedelta

			def __post_init__(self):
				#pylint: disable=no-member
				if not util.is_non_negative(self.num_record_limit):
					raise ValueError('flush_mode.num_record_limit', 'non-negative integer')
				if self.time_span_limit is not None and not isinstance(self.time_span_limit, timedelta):
					raise ValueError('flush_mode.time_span_limit', 'timedelta')

		MANUAL		= Params(0, None)
		IMMEDIATE	= Params(1, timedelta())
		FREQUENT	= Params(2000, timedelta(seconds=120))
		RARE		= Params(10000, timedelta(minutes=30))

	@unique
	class PersistMode(mixins.EnumParser, Enum):
		"""
		Indicates persistence mode to be used by the manager.
		"""
		DB			= auto()
		FILE		= auto()

	@unique
	class ProcessMode(mixins.EnumParser, Enum):
		"""
		Indicates type of process to be spawned by the manager.
		"""
		DETAIL		= auto()
		SCRAPE		= auto()


__all__ = [
	'interfaces',
	'invariants',
	'mixins'
]