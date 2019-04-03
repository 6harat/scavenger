from enum import Enum, unique
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from http import HTTPStatus
from scavenger.definitions.mixins import EnumMixin
from typing import Tuple, Type

@dataclass_json
@dataclass(frozen=True)
class ApiError:
	@unique
	class Message(EnumMixin, Enum):
		MISSING_OR_INVALID_PARAMETER	= (1, HTTPStatus.BAD_REQUEST)
		NOT_FOUND						= (2, HTTPStatus.NOT_FOUND)
		NO_OP_DURING_INITIALISATION		= (3, HTTPStatus.UNPROCESSABLE_ENTITY)

	@unique
	class Location(EnumMixin, Enum):
		BODY	= 'body'
		PATH	= 'path'
		QUERY	= 'query'

	@dataclass_json
	@dataclass(frozen=True)
	class Detail:
		location	:Type[ApiError.Location]
		field		:str
		description	:str

	message	:Type[Message]
	details	:Tuple[Detail]

	# utility functions
	@classmethod
	def build_invalid_param_error(cls, field, expected=None, location=None):
		message = cls.Message.MISSING_OR_INVALID_PARAMETER
		return dict(
				data=cls(
				message=message,
				details=(cls.Detail(
					location=cls.Location.BODY if not location else location,
					field=field,
					description='valid values: {}'.format(
						'non-empty string' if not expected else expected
					)
				),)
			), 
			status=message.value[1].value
		)

class DomainError:
	class ManagerAlreadyActivated(Exception): pass
	class FlushNotAllowed(Exception): pass
	class ManagerAlreadyFinished(Exception): pass

__all__ = [
	'ApiError',
	'DomainError'
]