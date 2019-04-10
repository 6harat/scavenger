from aiohttp import web
from scavenger.api import util
from scavenger.api.definitions import ApiError
from .validator import validator

import logging as log


@validator.flush
async def flush(request):
	"""
	Initiates flushing of records collected so far by the process.\n
	@query_params
		callback: get_url = None, for sending process completion notification
	"""
	pid, callback = (
		request.match_info.get('pid'),
		request.query.get('callback')
	)
	process = request.app['process_map'].get('pid')
	await process.flush()
	return web.json_response(None, status=202)

@validator.peek
async def peek(request):
	"""
	Reports the real-time details of the scraper process.\n
	@query_params
		show_records: bool = False, report collected app_ids if True
	"""
	pid, show_records = (
		request.match_info.get('pid'),
		util.parse_bool(request.query.get('show_records'))
	)
	process = request.app['process_map'].get(pid)

	return web.json_response(dict(
		logfile=request.app['logfile'],
		process=process.peek(show_records=show_records)
	), status=200)

@validator.peek_all
async def peek_all(request):
	"""
	Reports the real-time details of all scraper processes.\n
	@query_params
		show_finished: bool = False, include details of past processes if True
		show_records: bool = False, report collected app_ids for each manager if True
	"""
	show_finished, show_records = (
		util.parse_bool(request.query.get('show_finished')),
		util.parse_bool(request.query.get('show_records'))
	)
	processes = request.app['process_map'].values()
	if not show_finished:
		processes = filter(lambda p: not p.is_finished(), processes)
	if not processes:
		raise ApiError(404)

	return web.json_response(dict(
		logfile=request.app['logfile'],
		processes=list(map(
			lambda p: p.peek(show_records=show_records),
			processes.values()
		))
	), status=200)

@validator.start
async def start(request):
	"""
	Activates a process based on configurations passed in the body.
	"""
	pass

@validator.stop
async def stop(request):
	"""
	Initiates termination of the process.\n
	@query_params
		callback: get_url = None, for sending process completion notification
	"""
	pid, callback = (
		request.match_info.get('pid'),
		request.query.get('callback')
	)
	process = request.app['process_map'].get('pid')
	await process.terminate()
	return web.json_response(None, status=202)

@validator.update
async def update(request):
	pid = request.match_info.get('pid')
	process = request.app['process_map'].get(pid)
	return web.json_response(None, status=200)


__all__ = [
	'flush',
	'peek',
	'peek_all',
	'start',
	'stop',
	'update'
]
