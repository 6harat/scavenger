from aiohttp import web
from scavenger.api.definitions import ApiError, Detail
from scavenger.core.definitions import DomainError

@web.middleware
async def error_middleware(request, handler):
	try:
		return await handler(request)
	except ApiError as ae:
		return ae.to_web_response()
	except DomainError as de:
		return ApiError(
			de.status, 
			(Detail(de.name, de.message),)
		).to_web_response()

__all__ = [
	'error_middleware'
]