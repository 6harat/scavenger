import abc

class JsonSerializable_:
	@abc.abstractclassmethod
	def from_json(cls, data):
		raise NotImplementedError
	
	@abc.abstractmethod
	def to_json(self):
		raise NotImplementedError

__all__ = [
	'JsonSerializable_'
]