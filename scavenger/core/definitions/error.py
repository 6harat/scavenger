from enum import unique, Enum

class DomainError(Exception, Enum):
	PROCESS_ALREADY_ACTIVATED	= (422, 'Process already activated or being activated.')
	FLUSH_NOT_ALLOWED			= (422, 'Flush only allowed when the process is running.')

	@property
	def status(self):
		return super().args[0]
	
	@property
	def message(self):
		return super().args[1]

	def __init__(self, status, message):
		super().__init__(status, message)

__all__ = [
	'DomainError'
]