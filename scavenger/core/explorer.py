from scavenger.core.definitions import Processor_, Status
from scavenger.core import Flusher


class Explorer(Processor_):

	def __init__(self, uid, flusher: Flusher):
		self.__uid__ = uid
		self.__started_at__ = datetime.now()
		self.__stopped_at__ = None
		self.__status__ = Status.INITIATING
		self.__process_mode__ = process_mode
		self.__store__ = Store()
		self.__flusher__ = flusher
		self.__persistor__ = 
		self.__fetcher__ = None
		self.__subscriptions__ = None
		self.__tasks__ = None
		self.__post_init__()

	@property
	def uid(self):
		return self.__uid__

	@property
	def process_mode(self):
		return self.__process_mode__

	@property
	def status(self):
		return self.__status__

	def __register_subscriptions__(self):
		self.__subscriptions__ = (
			self.__store__.subscribe(self.__flusher__),
			self.__flusher__.subscribe(self.__persistor__)
		)

	# concrete async methods
	async def activate(self):
		if self.status != self.__class__.Status.INITIATING:
			raise err.ManagerAlreadyActivated
		async with PlayFetch(persist=True) as fetcher:
			self.__fetcher__ = fetcher
			self.__register_subscriptions__tas()
			await self.__execute__()

	async def flush(self):
		if self.status != self.__class__.Status.INITIATING:
			raise err.FlushNotAllowed
		self.__flusher__.purge(forced=True)
		return self.peek()

	async def terminate(self):
		if self.is_finished():
			raise err.ManagerAlreadyFinished
		log.info('terminating manager')
		await self.__shutdown__(forced=True)

	async def __shutdown__(self,  forced=False):
		if forced: self.__status__ = self.__class__.Status.TERMINATING
		else: self.__status__ = self.__class__.Status.SHUTTING

		self.__fetcher__.force_close()
		self.

	# concrete sync methods
	def is_pending(self):
		return self.status in [
			self.__class__.Status.INITIATING,
			self.__class__.Status.RUNNING,
			self.__class__.Status.SHUTTING,
			self.__class__.Status.TERMINATING
		]

	def is_finished(self):
		return self.status in [
			self.__class__.Status.FAILED,
			self.__class__.Status.TERMINATED,
			self.__class__.Status.COMPLETED
		]

	def __create_task__(self, coro, shield=False):
		return
