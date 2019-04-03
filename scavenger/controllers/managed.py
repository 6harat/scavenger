from aiohttp import web
from scavenger.adapter import PlayFetch, Utils
from scavenger.definitions.manager import Manager_
from scavenger.definitions.proxy import ProxyManager
from scavenger.helper import constants, is_empty, is_str_in, is_true
from uuid import uuid4 as uidgen

import logging as log

async def peek(request):
	pid = request.match_info.get('pid')
	show_records = is_true(request.query.get('show_records'))
	if is_empty(pid):
		return web.json_response(dict(
			message='MISSING_REQUIRED_PARAMETER',
			location='path',
			field='pid'
		), status=400)
	manager = request.app['managers'].get(pid)
	if not manager:
		return web.json_response(dict(
			message='NOT_FOUND',
		), status=404)
	opt = manager.peek(show_records=show_records)
	return web.json_response(dict(
		message='MANAGER_PEEKED',
		logfile=constants.get('log').get('file_path'),
		**opt
	))

async def peek_all(request):
	show_records = is_true(request.query.get('show_records'))
	managers = request.app['managers']
	if not managers:
		return web.json_response(dict(
			message='NOT_FOUND',
		), status=404)
	return web.json_response(dict(
		message='ALL_MANAGERS_PEEKED',
		logfile=constants.get('log').get('file_path'),
		managers=list(map(
			lambda mgr: mgr.peek(show_records=show_records),
			managers.values()
		))
	))

def build_invalid_param_error(field, expected):
	return dict(
		message='MISSING_REQUIRED_PARAMETER',
		location='body',
		field=field,
		details='{} should be one of {}'.format(
			field, expected
		)
	)

async def _validate_and_inject(request):
	errors = []
	# validate input
	action = Manager_.Action.parse(request.query.get('action'))
	if action is None:
		errors.append(dict(
			message='INVALID_PARAMETER_VALUE',
			location='query',
			field='action',
			details='action should one of {}'.format(Manager_.Action.all_names())
		), status=400)
		return errors, None

	params = await request.post()
	if action != 'start':
		if is_empty(params.get('pid')):
			errors.append(dict(
				message='MISSING_REQUIRED_PARAMETER',
				location='body',
				field='pid'
			))
	else:
		process_mode = Manager_.ProcessMode.parse(params.get('type'))
		if process_mode is None:
			error.append(build_invalid_param_error(
				field='type', expected=Manager_.ProcessMode.all_names()
			))
		else:
			params.update(type=process_mode)
		
		store = Manager_.Store.parse(params.get('store'))
		if store is None:

	# inject defaults
	if not errors:
		params.update(
			action=action,
			uid=str(uidgen())
		)
	return errors

async def execute(request):
	err, params = await _validate_and_inject(request)
	if err:
		return web.json_response(dict(
			message='INVALID_PARAMETER_VALUE',
			details=err
		))
	mgr = ProxyManager()
	
