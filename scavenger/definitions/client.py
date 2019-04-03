from aiohttp import ClientSession, ClientTimeout
from dataclasses import dataclass
from typing import Dict, Type

import logging as log

@dataclass
class PersistableClient:
	"""
	a client whose connection can be persisted
	"""
	_headers: Dict
	_session: Type[ClientSession]
	_timeout: Type[ClientTimeout]
	_persist: bool = False

	async def __aenter__(self):
		self._session = ClientSession(
			headers=self._headers,
			timeout=self._timeout
		)
		return self
	async def __aexit__(self, *err):
		if not self._persist:
			await self._session.close()
			self._session = None

	async def force_close(self):
		if self._session and not self._session.closed:
			try:
				await self._session.close()
			except:
				log.warning('session already closed')
			finally:
				self._session = None

__all__ = [
	'PersistableClient'
]