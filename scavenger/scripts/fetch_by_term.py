from scavenger.adapter import PlayFetch
from scavenger.helper import initialize
import asyncio
import json
import logging as log
import math

initialize()

def load_emails():
	with open('../email.txt') as f:
		return { l.strip() for l in f.readlines() }

def load_dev_ids():
	with open('../dev.txt') as fd:
		return { l.strip() for l in fd.readlines() }

old_emails_set = load_emails()
old_emails = list(old_emails_set)
old_dev_ids_set = load_dev_ids()
log.info('old emails: {} and dev ids: {} loaded'.format(
	len(old_emails_set), len(old_dev_ids_set))
)
info_map = dict()
discarded = set()

async def process_app(r):
	dev_id = r.get('developer_id')
	log.info('processing dev_id: {}'.format(dev_id))
	if dev_id not in old_dev_ids_set and dev_id not in discarded and dev_id not in info_map:
		app_id = r.get('app_id')
		async with PlayFetch() as detail_fetcher:
			try:
				detail = await detail_fetcher.get_app_details(app_id)
			except:
				log.warning('failed to fetch app_detail for: {}'.format(app_id))
			else:
				email = detail.get('developer_email')
				if email not in old_emails_set:
					log.info('adding dev_id: {} and email: {} to info_map'.format(dev_id, email))
					old_emails_set.add(email)
					info_map[dev_id] = dict(
						dev_id=dev_id, app_id=app_id, email=email
					)
				else:
					log.info('discarding dev_id: {}'.format(dev_id))
					discarded.add(dev_id)
	else:
		log.info('skipping dev_id: {}'.format(dev_id))
		
def dump_data(idx):
	log.info('data dump started')
	try:
		with open('../dev_info.{}.json'.format(idx), 'w') as wf:
			json.dump(info_map, wf)
	except:
		log.info('data dump failed')
	else:
		log.info('data dump finished')

async def search_by_term(fetcher, term):
	try:
		log.info('searching for term: {}'.format(term))
		results = await fetcher.search(term, max_page=5)
	except:
		log.warning('failed to fetch search results')
	else:
		await asyncio.gather(*[ process_app(r) for r in results ])

async def main(terms, idx):
	log.info('started process for idx: {}'.format(idx))
	async with PlayFetch() as fetcher:
		await asyncio.gather(*[ search_by_term(fetcher, term) for term in terms ])
	dump_data(idx)

loop = asyncio.get_event_loop()
go = lambda idx, count=10000: loop.run_until_complete(main(
	old_emails[idx*count:(idx+1)*count],
	idx
))
goc = lambda: loop.run_until_complete(main(
	'abcdefghijklmnopqrstuvwxyz',
	2
))
def gow():
	try:
		with open('../words_alpha.txt') as wf:
			words = [ e.strip() for e in wf.readlines()]
	except:
		log.error('failed to load words')
	else:
		len_words = len(words)
		log.info('loaded words: {}'.format(len_words))
		chunk_size = 1000
		num_chunks = math.ceil(len_words/chunk_size)
		log.info('initiating search, chunk_size: {} num_chunks: {}'.format(
			chunk_size, num_chunks
		))
		for i in range(num_chunks):
			loop.run_until_complete(main(
				words[i*chunk_size: (i+1)*chunk_size],
				'words_{}'.format(i)
			))
	