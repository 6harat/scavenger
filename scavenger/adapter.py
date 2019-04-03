from aiohttp import ClientResponseError, ClientTimeout
from bs4 import BeautifulSoup, SoupStrainer
from pydash import omit
from scavenger.definitions import Fetcher_, PersistableClient
from scavenger.helper import prune_records
from urllib.parse import parse_qs, quote_plus, urlparse

import asyncio
import functools
import logging as log
import play_scraper as ps

sem = asyncio.Semaphore(40)

class Utils:
	_UNWANTED_KEYS = [
		'description_html',
		'screenshots',
		'video',
		'histogram',
		'interactive_elements',
		'recent_changes'
	]
	_MAX_SEARCH_PAGE_LIMIT = 5
	_PAGINATED_SEARCH_URL = 'https://play.google.com/store/apps/collection/search_results_cluster_apps?gsr={gsr}&authuser=0'
	_PAGE_TOKENS = [
		'-p6BnQMCCDE=:S:ANO1ljJ4Cw8',
		'-p6BnQMCCGI=:S:ANO1ljJYYFs',
		'-p6BnQMDCJMB:S:ANO1ljLvbuA',
		'-p6BnQMDCMQB:S:ANO1ljIeRbo',
		'-p6BnQMDCPUB:S:ANO1ljKG00U'
	]
	_PAGE_NUM_SIZE = 48

	@staticmethod
	def pruned(func):
		async def executor(*args, **kwargs):
			opt = await func(*args, **kwargs)
			return prune_records(opt, Utils._UNWANTED_KEYS)
		return executor

	@staticmethod
	def retrieve_search_params(soup):
		if not soup:
			return None
		href = soup[0].attrs['href']
		return parse_qs(urlparse(href).query)
	
	@staticmethod
	def get_paginated_search_post_data(clp, page):
		return dict(
			start=page * Utils._PAGE_NUM_SIZE,
			num=Utils._PAGE_NUM_SIZE,
			numChildren=0,
			pagTok=Utils._PAGE_TOKENS[page],
			clp=clp,
			pagtt=3,
			cctcss='square-cover',
			cllayout='NORMAL',
			ipf=1,
			xhr=1
		)

	@staticmethod
	def get_paginated_search_params(soup, max_page):
		if max_page == 1:
			return None
		search_configs = Utils.retrieve_search_params(soup.select('[data-uitype="291"]'))
		if not search_configs:
			log.warning('unable to retrieve gsr value for fetching next pages')
			return None
		post_data_gen = functools.partial(Utils.get_paginated_search_post_data, search_configs.get('clp'))
		return dict(
			url=Utils._PAGINATED_SEARCH_URL.format(gsr=search_configs.get('gsr')),
			datas=[ post_data_gen(page) for page in range(max_page-1) ]
		)
		
	@staticmethod
	async def parse_fetched_response(awaitable_process, multi=True):
		soup = None
		try:
			response = await awaitable_process()
			soup = BeautifulSoup(response, 'lxml')
		except ClientResponseError:
			log.exception('no records returned')
		if soup is None:
			return None

		if multi:
			opt = list(map(
				ps.utils.parse_card_info, 
				soup.select('div[data-uitype="500"]')
			))
		else:
			opt = ps.utils.parse_app_details(soup)

		return (soup, opt)

class PlayFetch(Fetcher_, PersistableClient):
	def __init__(self, persist=False, headers=ps.utils.default_headers(), timeout=30, hl='en', gl='us'):
		self._headers = headers
		self._timeout = ClientTimeout(total=timeout)
		self._params = dict(hl=hl, gl=gl)
		self._persist = persist

	async def send_request(self, method, url, data=None, params={}, allow_redirects=False):
		options = dict(
			method=method,
			url=url,
			params=params,
			data=ps.utils.generate_post_data() if not data and method == 'POST' else data,
			allow_redirects=allow_redirects
		)
		async with sem:
			log.info('sending request to url: {}'.format(url))
			async with self._session.request(**options) as response:
				response.raise_for_status()
				return await response.text()
	
	@Utils.pruned
	async def get_app_details(self, app_id):
		url = ps.utils.build_url('details', app_id)

		awaitable_process = functools.partial(self.send_request, 'GET', url, params=self._params)
		result = await Utils.parse_fetched_response(awaitable_process, multi=False)
		if not result:
			log.warning('no data found for app_id: {}'.format(app_id))
			return {}
		
		_, app_json = result
		app_json.update({
			'app_id': app_id,
			'url': url
		})
		return app_json

	@Utils.pruned
	async def get_apps(self, coln_id, catg_id, results=None, page=None):
		coln_name = coln_id if coln_id.startswith('promotion') else ps.lists.COLLECTIONS.get(coln_id)
		if coln_name is None:
			raise ValueError('INVALID_COLLECTION_ID: {coln}'.format(
				coln=coln_id
			))

		catg_name = '' if catg_id is None else ps.lists.CATEGORIES.get(catg_id)
		if catg_name is None:
			raise ValueError('INVALID_CATEGORY_ID: {catg}'.format(
				catg=catg_id
			))
		results = ps.settings.NUM_RESULTS if results is None else results
		if results > 120:
			raise ValueError('Number of results cannot be more than 120.')

		page = 0 if page is None else page
		if page * results > 500:
			raise ValueError('Start (page * results) cannot be greater than 500.')

		url = ps.utils.build_collection_url(catg_name, coln_name)
		data = ps.utils.generate_post_data(results, page)
		
		awaitable_process = functools.partial(self.send_request, 'POST', url, data, params=self._params)
		result = await Utils.parse_fetched_response(awaitable_process)
		if not result:
			log.warning('no apps found for coln_id: {} and catg_id: {}'.format(
				coln_id, catg_id
			))
			return []
		
		_, apps = result
		return apps
	
	@Utils.pruned
	async def get_similar_apps(self, app_id):
		url = ps.utils.build_url('similar', app_id)
		
		awaitable_process = functools.partial(self.send_request, 'GET', url, params=self._params, allow_redirects=True)
		result = await Utils.parse_fetched_response(awaitable_process)
		if not result:
			log.warning('no similar apps found for app_id: {}'.format(app_id))
			return []
		
		_, apps = result
		return apps
	
	@Utils.pruned
	async def search(self, term, max_page=1):
		if not (1 <= max_page <= Utils._MAX_SEARCH_PAGE_LIMIT):
			raise ValueError('max_page: {} should be between 1 and {}'.format(
				max_page,
				Utils._MAX_SEARCH_PAGE_LIMIT
			))
		url = '{url}?c=apps&q={query}'.format(
			query=quote_plus(term),
			url=ps.settings.SEARCH_URL
		)
		awaitable_process = functools.partial(self.send_request, 'GET', url, params=self._params)
		result = await Utils.parse_fetched_response(awaitable_process)
		if not result:
			log.warning('no serach results found for term: {}'.format(term))
			return []
		
		soup, apps = result
		search_params = Utils.get_paginated_search_params(soup, max_page)
		if not search_params:
			return apps
		
		tasks = [
			Utils.parse_fetched_response(functools.partial(
				self.send_request,
				'POST',
				search_params.get('url'), 
				data, 
				params=self._params
			))
			for data in search_params.get('datas')
		]
		task_results = await asyncio.gather(*tasks)
		if not task_results:
			return apps

		for _, tapps in task_results:
			apps.extend(tapps)
		
		return apps
