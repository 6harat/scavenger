from aiohttp import web
from pydash import pick
from scavenger.helper import constants, initialize
from scavenger.middleware import auth_middleware, error_middleware
from scavenger.routes import routes

import asyncio
import json
import logging as log

async def on_startup(app):
	pass

async def on_shutdown(app):
	pass

if __name__ == '__main__':
	initialize()
	app = web.Application(middlewares=[
		error_middleware,
		auth_middleware
	])
	app.on_startup.append(on_startup)
	app.on_shutdown.append(on_shutdown)
	app.add_routes(routes)
	web.run_app(app, **pick(
		constants.get('info'), 'host', 'port'
	))
