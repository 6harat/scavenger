from scavenger.managers.base import BaseManager_

import play_scraper as ps

class Crawler(BaseManager_):
	def peek(self, show_records=False):
		pass

	async def __execute__(self):
		for coln in ps.lists.COLLECTIONS:
			for catg in ps.lists.CATEGORIES:
				self.__register_task