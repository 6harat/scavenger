from rx.subjects import Subject

import logging as log

class Store(Subject):
	def __init__(self):
		super().__init__()
		self.__bucket__ = set()
		self.__num_records__ = 0

	@property
	def num_records(self):
		return self.__num_records__

	def on_next(self, key, value):
		if key not in self.__bucket__:
			self.__bucket__.add(key)
			self.__num_records__ += 1
			super().on_next(value)

	def on_error(self, error):
		# no_op as the error will be handled by the manager itself
		return None

	def on_completed(self):
		return super().on_completed()

__all__ = [
	'Store'
]