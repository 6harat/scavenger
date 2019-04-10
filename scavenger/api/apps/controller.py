from aiohttp import web
from playmate import PlayMate
from scavenger.api import props, util
from .validator import validator

import logging as log


@validator.apps
async def apps(request):
	"""
	Retrieves apps from the app store.\n
	@query_params
		coln_id: str, used in combination with catg_id
		catg_id: str, used in combination with coln_id
		term: str, used as a free-form search string
		max_page: int, number of pages to be fetched
	"""
	coln_id, catg_id, term, max_page = (
		request.query.get('coln_id'),
		request.query.get('catg_id'),
		request.query.get('term'),
		util.parse_int(
			request.query.get('max_page'),
			default=props.apps.page_limit.minimum
		)
	)
	log.info('fetching apps for: {}'.format(request.query))
	async with PlayMate() as mate:
		opt = await (mate.search_apps(
			term, max_page=max_page
		) if term else mate.get_apps(
			coln_id, catg_id, max_page=max_page
		))
		return web.json_response(opt)

@validator.detail
async def detail(request):
	"""
	Retrieves details for an app_id
	"""
	app_id = request.match_info.get('app_id')
	log.info('fetching detail for: {}'.format(app_id))
	async with PlayMate() as mate:
		opt = await mate.get_app_details(app_id)
		return web.json_response(opt)

@validator.similar
async def similar(request):
	"""
	Retrieves other apps similar to app_id
	"""
	app_id = request.match_info.get('app_id')
	log.info('fetching similar apps for: {}'.format(app_id))
	async with PlayMate() as mate:
		opt = await mate.get_similar_apps(app_id)
		return web.json_response(opt)


__all__ = [
	'apps',
	'detail',
	'similar'
]