import abc

class Fetcher_(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	async def send_request(self, method, url, data=None, params={}, allow_redirects=False):
		raise NotImplementedError

	@abc.abstractmethod
	async def get_app_details(self, app_id):
		raise NotImplementedError

	@abc.abstractmethod
	async def get_apps(self, coln_id, catg_id, results=None, page=None):
		raise NotImplementedError

	@abc.abstractmethod
	async def get_similar_apps(self, app_id):
		raise NotImplementedError

	@abc.abstractmethod
	async def search(self, term, page=0):
		raise NotImplementedError

__all__ = [
	'Fetcher_'
]