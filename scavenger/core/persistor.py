from collections.abc import Iterable
from enum import unique, Enum
from pymongo import errors as pymerr
from rx.core import Observer
from scavenger.definitions.mixins import EnumParserMixin
from scavenger.helper import constants

import asyncio
import logging as log
import motor.motor_asyncio

class AppInfoDao:
	def get(app_id:str) -> dict:
		pass

	def get_all() -> list:
		pass

	def save(app_info:dict) -> None:
		pass

	def update(app_info:dict, partial:bool=True) -> None:
		pass

	def delete(app_id:str)	-> None:
		pass


class OpInfoDao:
	pass


class Persistor(Observer):
	def __init__(self):
		log.debug('opening db connection')
		self.__client__ = motor.motor_asyncio.AsyncIOMotorClient(
			constants.get('db').get('url')
		)
		self.__collection__ = self.__client__.get(
			constants.get('db').get('name')).get('play_store_apps')
		self.__loop__ = asyncio.get_event_loop()

	async def __execute__(self, values):
		try:
			await self.__collection__.insert_many(
				Transformer.to_db(values), 
				ordered=False
			)
		except pymerr.BulkWriteError:
			log.warning('skipped duplicate records')
		except:
			log.exception('unknown db error was encountered')
	
	def on_next(self, values):
		self.__loop__.create_task(self.__execute__(values))

	def on_completed(self):
		log.debug('closing db connection')
		self.__client__.close()

class Loader(Observer):
	pass
	