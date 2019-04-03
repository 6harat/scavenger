from aiohttp import web
from scavenger.controllers import core, managed

routes = [
	# core services
	web.get('/detail', core.detail),
	web.get('/apps', core.apps),
	web.get('/similar', core.similar),
	web.get('/search', core.search),

	# managed services
	web.get('/manager/peek', managed.peek_all),
	web.get('/manager/{pid}/peek', managed.peek),
	web.post('/manager', managed.execute)
]