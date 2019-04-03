from dataclasses import dataclass
from enum import auto, Enum, unique
from scavenger.data_sources import DbPersistor, FilePersistor
from scavenger.definitions.mixins import EnumParserMixin
from typing import Type

import abc
import functools

class Manager_:
	# enums
	@unique
	class Action(EnumParserMixin, Enum):
		START		= auto()
		STOP		= auto()
		FLUSH		= auto()

	@unique
	class ProcessMode(EnumParserMixin, Enum):
		DETAIL		= auto()
		CRAWL		= auto()

	@unique
	class PersistMode(EnumParserMixin, Enum):
		DB			= functools.partial(DbPersistor)
		FILE		= functools.partial(FilePersistor)
	
	@unique
	class Status(EnumParserMixin, Enum):
		INITIATING	= auto()
		INITIATED	= auto()
		RUNNING		= auto()
		FLUSHING	= auto()
		SHUTTING	= auto()
		TERMINATING	= auto()
		FAILED		= auto()
		TERMINATED	= auto()
		COMPLETED	= auto()
		
	# async methods
	@abc.abstractmethod
	async def activate(self):
		raise NotImplementedError

	@abc.abstractmethod
	async def flush(self):
		raise NotImplementedError

	@abc.abstractmethod
	async def terminate(self):
		raise NotImplementedError

	# sync methods
	@abc.abstractmethod
	def is_pending(self):
		raise NotImplementedError
	
	@abc.abstractmethod
	def is_finished(self):
		raise NotImplementedError

	@abc.abstractmethod
	def peek(self, show_records=False):
		raise NotImplementedError

	# internal async methods
	@abc.abstractmethod
	async def __execute__(self):
		raise NotImplementedError

	@abc.abstractmethod
	async def __shutdown__(self, forced=False):
		raise NotImplementedError

	# internal sync methods
	@abc.abstractmethod
	def __post_init__(self):
		pass

	@abc.abstractmethod
	def __create_task__(self, coro, shield=False):
		raise NotImplementedError
	
__all__ = [
	'Manager_'
]