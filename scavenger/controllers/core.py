from aiohttp import web
from scavenger.adapter import PlayFetch, Utils
from scavenger.definitions.error import ApiError as err
from scavenger.helper import parse_int

import logging as log

async def detail(request):
	app_id = request.query.get('app_id')
	if app_id is None:
		return web.json_response(**err.build_invalid_param_error(
			field='app_id', location=err.Location.QUERY
		))
	log.info('fetching detail for: {}'.format(
		app_id
	))
	async with PlayFetch() as fetcher:
		opt = await fetcher.get_app_details(app_id)
		return web.json_response(opt)

async def apps(request):
	coln_id = request.query.get('coln_id')
	catg_id = request.query.get('catg_id')
	page = parse_int(request.query.get('page'), default=0)
	results = parse_int(request.query.get('results'), default=120)
	if coln_id is None or catg_id is None:
		return web.json_response(dict(
			message='MISSING_REQUIRED_PARAMETER',
			location='query',
			field=['coln_id', 'catg_id']
		), status=400)
	if results > 120 or page * results > 500:
		return web.json_response(dict(
			message='INVALID_PARAMETER_VALUE',
			location='query',
			field=['page', 'results'],
			details='results should be [1, 120] and (page * results) should be [1, 500]'
		), status=400)
	log.info('fetching apps for coln: {}; catg: {}; page: {}; results: {}'.format(coln_id, catg_id, page, results))
	async with PlayFetch() as fetcher:
		opt = await fetcher.get_apps(coln_id, catg_id, results=results, page=page)
		return web.json_response(opt)

async def similar(request):
	app_id = request.query.get('app_id')
	if app_id is None:
		return web.json_response(dict(
			message='MISSING_REQUIRED_PARAMETER',
			location='query',
			field='app_id'
		), status=400)
	log.info('fetching similar for: {}'.format(app_id))
	async with PlayFetch() as fetcher:
		opt = await fetcher.get_similar_apps(app_id)
		return web.json_response(opt)

async def search(request):
	term = request.query.get('term')
	max_page = parse_int(request.query.get('max_page'), default=1)
	if term is None:
		return web.json_response(dict(
			message='MISSING_REQUIRED_PARAMETER',
			location='query',
			field='term'
		), status=400)
	if not (1 <= max_page <= Utils._MAX_SEARCH_PAGE_LIMIT):
		return web.json_response(dict(
			message='INVALID_PARAMETER_VALUE',
			location='query',
			field='max_page',
			details='max_page should be [1, 5]'
		), status=400)
	log.info('fetching search result for term: {}; max_page: {}'.format(term, max_page))
	async with PlayFetch() as fetcher:
		opt = await fetcher.search(term, max_page=max_page)
		return web.json_response(opt)
