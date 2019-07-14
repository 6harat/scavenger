from aiohttp import web
from enum import auto, Enum, unique
from dataclasses import dataclass, field
from http import HTTPStatus
from scavenger.api import util
from scavenger.api.definitions import mixins
from typing import Iterable, Tuple, Union

@unique
class Location(mixins.EnumParser, Enum):
	BODY	= 'body'
	PATH	= 'path'
	QUERY	= 'query'

@unique
class Issue(mixins.EnumParser, Enum):
	ARGS_NOT_SUPPORTED			= (1, lambda scenario=None: 'supported only when: {}'.format(
		'' if util.is_empty(scenario) else scenario
	))
	INVALID_PARAMETER_VALUE		= (2, lambda expected=None: 'valid values: {}'.format(
		'non-empty string' if util.is_empty(expected) else expected
	))
	NOT_FOUND					= (3, lambda : 'requested resource not found')

	def __description__(self):
		#pylint: disable=unsubscriptable-object
		return self.value[1]

@dataclass(frozen=True)
class Detail:
	issue		:str
	description	:str
	field		:str	= None
	location	:str	= None

	def __post_init__(self):
		if self.field is not None and self.location is None:
			object.__setattr__(self, 'location', Location.QUERY.value)
	
	@classmethod
	def build(cls, issue: Union[str, Issue], field:str=None, location:Location=None, **desc_args) -> 'Detail':
		parsed_issue = Issue.parse(issue)
		parsed_location = Location.parse(location)
		if parsed_issue is None:
			raise ValueError('not a valid Issue: {}'.format(issue))
		if location is not None and parsed_location is None:
			raise ValueError('not a valid Location: {}'.format(location))
		return cls(issue.name, issue.__description__()(**desc_args), field, location.value if location else None)

@dataclass(frozen=True)
class ApiError(Exception):
	status	:Union[int, HTTPStatus]
	details	:Iterable[Detail]

	def __post_init__(self):
		if isinstance(self.status, int):
			object.__setattr__(self, 'status', HTTPStatus(self.status))
		if not isinstance(self.details, tuple):
			object.__setattr__(self, 'details', tuple(self.details))

	# utility functions
	def to_web_response(self):
		return web.json_response(
			tuple(map(lambda d: d.__dict__, self.details)),
			status=self.status.value
		)


__all__ = [
	'ApiError',
	'Detail',
	'Issue',
	'Location'
]