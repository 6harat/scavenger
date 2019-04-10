from playmate import PlayMate
from scavenger.helper import initialize
import asyncio
import json
import logging as log
import math

initialize()

EMAIL_FILE_PATH		= '../../static/emails.txt'
DEV_IDS_FILE_PATH	= '../../static/devs.txt'
DICT_WORD_FILE_PATH	= '../../static/words_alpha.txt'
OPT_FILE_PATH		= '../../opt/app_info_{suffix}.json'


def load_emails():
	try:
		with open(EMAIL_FILE_PATH) as fe:
			return { l.strip() for l in fe.readlines() }
	except:
		log.exception('failed to load past emails')
		return set()

def load_dev_ids():
	try:
		with open(DEV_IDS_FILE_PATH) as fd:
			return { l.strip() for l in fd.readlines() }
	except:
		log.exception('failed to load past developer ids')
		return set()

def load_dict_words():
	try:
		with open(DICT_WORD_FILE_PATH) as fw:
			return [ e.strip() for e in fw.readlines()]
	except:
		log.exception('failed to load dict words')
		return []

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
		async with PlayMate() as detail_fetcher:
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
		with open(OPT_FILE_PATH.format(suffix=idx), 'w') as wf:
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
	async with PlayMate() as fetcher:
		await asyncio.gather(*[ search_by_term(fetcher, term) for term in terms ])
	dump_data(idx)

loop = asyncio.get_event_loop()

gochar = lambda: loop.run_until_complete(main(
	'abcdefghijklmnopqrstuvwxyz',
	'char'
))
def goword():
	words = load_dict_words()
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
			'word_{}'.format(i)
		))
