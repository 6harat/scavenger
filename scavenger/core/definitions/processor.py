from scavenger.core.definitions import Proxy

import abc
import functools

class Processor_:

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
	
class ProcessorProxy(Proxy, Processor_):
	pass

__all__ = [
	'Processor_',
	'ProcessorProxy'
]