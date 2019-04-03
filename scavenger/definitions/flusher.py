from dataclasses import dataclass
from datetime import datetime, timedelta
from rx.subjects import Subject
from typing import List, Type

import logging as log

class Flusher(Subject):

	@dataclass(frozen=True)
	class Mode:
		num_records		:int
		duration		:Type[timedelta]

		def __post__init__(self):
			if self.num_records is not None and self.num_records < 0:
				raise ValueError('num_records should be a non-negative integer')
			if self.duration is not None and not isinstance(self.duration, timedelta):
				raise ValueError('duration should be a valid datetime.timedelta')

		def should_flush(self, curr_records, curr_duration):
			return (self.num_records is not None and curr_records >= self.num_records) or (
					self.duration is not None and curr_duration >= self.duration)

	def __init__(self, flush_mode:Type[Mode]):
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