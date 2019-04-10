from dataclasses import dataclass
from typing import Any

@dataclass
class Proxy:
	_obj:Any
	def __getattribute__(self, name):
		return object.__getattribute__(self, name) if (name == '_obj') else object.__getattribute__(self._obj, name)
	def __setattr__(self, name, value):
		if (name == '_obj'): object.__setattr__(self, name, value)
		else: object.__setattr__(self._obj, name, value)
	def __delattr__(self, name):
		delattr(self._obj, name)
	def __nonzero__(self):
		return bool(self._obj)
	def __str__(self):
		return str(self._obj)
	def __repr__(self):
		return repr(self._obj)
	def __hash__(self):
		return hash(self._obj)

__all__ = [
	'Proxy'
]