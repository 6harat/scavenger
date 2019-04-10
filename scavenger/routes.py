from aiohttp import web
from scavenger.api import apps, scraper

routes = [
	# apps services
	web.get('/apps', apps.apps),
	web.get('/apps/{app_id}/detail', apps.detail),
	web.get('/apps/{app_id}/similar', apps.similar),

	# scraper services
	web.post('/scraper/{pid}', scraper.flush),
	web.get('/scraper/{pid}', scraper.peek),
	web.get('/scraper', scraper.peek_all),
	web.post('/scraper', scraper.start),
	web.delete('/scraper/{pid}', scraper.stop),
	web.patch('/scraper/{pid}', scraper.update),
]