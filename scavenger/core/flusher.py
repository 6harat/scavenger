from dataclasses import dataclass
from datetime import datetime, timedelta
from rx.subjects import Subject
from scavenger.api.definitions import invariants
import logging as log

class Flusher(Subject):

	def __init__(self, flush_mode:invariants.FlushMode.Params):
		self.__flush_mode__ = flush_mode
		self.__container__ = []
		self.__num_records__ = 0
		self.__last_flushed__ = datetime.now()

	def purge(self, forced=False):
		curr_datetime = datetime.now()
		if forced or self.__flush_mode__.should_flush(self.__num_records__, curr_datetime - self.__last_flushed__):
			self.__last_flushed__ = curr_datetime
			records = list(self.__container__)
			self.__container__.clear()
			self.__num_records__ = 0
			if records:
				super().on_next(records)

	def on_next(self, value):
		self.__container__.append(value)
		self.__num_records__ += 1
		self.purge()
	
	def on_error(self, err):
		pass

	def on_completed(self):
		self.purge(forced=True)
		super().on_completed()

__all__ = [
	'Flusher'
]