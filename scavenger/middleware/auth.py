from aiohttp import web
from scavenger.api.definitions import ApiError, Detail, Issue

recognized_keys = {
	'95e50751-92dc-46c1-9a34-449d32a3e40d',
}

@web.middleware
async def auth_middleware(request, handler):
	if request.headers.get('api_key') not in recognized_keys:
		raise ApiError(
			status=404,
			details=(Detail.build(Issue.NOT_FOUND),)
		)
	return await handler(request)

__all__ = [
	'auth_middleware'
]