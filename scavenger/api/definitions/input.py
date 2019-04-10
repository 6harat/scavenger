from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from scavenger.api import util
from scavenger.api.definitions import ApiError, Detail, Issue, Location, invariants
from typing import Any, Union

@dataclass_json
@dataclass(frozen=True)
class ProcessArgs:
	pid				:str = field(default_factory=util.uid_gen)
	process_mode    :invariants.ProcessMode = invariants.ProcessMode.SCRAPE
	persist_mode    :invariants.PersistMode = invariants.PersistMode.DB
	flush_mode		:invariants.FlushMode.Params = invariants.FlushMode.FREQUENT.value

	def __post_init__(self):
		err_details = []
		_process_mode = invariants.ProcessMode.parse(self.process_mode)
		if _process_mode is None:
			err_details.append(Detail.build(
				Issue.INVALID_PARAMETER_VALUE,
				field='process_mode',
				location=Location.BODY,
				expected=invariants.ProcessMode.all_names()
			))
		_persist_mode = invariants.PersistMode.parse(self.persist_mode)
		if _persist_mode is None:
			err_details.append(Detail.build(
				Issue.INVALID_PARAMETER_VALUE,
				field='persist_mode',
				location=Location.BODY,
				expected=invariants.PersistMode.all_names()
			))
		_flush_mode = invariants.FlushMode.parse(self.flush_mode) or invariants.FlushMode.Params.from_json(self.flush_mode)
		if _flush_mode is None:
			err_details.append(Detail.build(
				Issue.INVALID_PARAMETER_VALUE,
				field='flush_mode',
				location=Location.BODY,
				expected='{} or valid FlushMode.Params'.format(invariants.FlushMode.all_names())
			))
		
		if err_details:
			raise ApiError(
				status=400,
				details=err_details
			)

		# inject parsed values if all validation succeeds
		object.__setattr__(self, 'process_mode', _persist_mode)
		object.__setattr__(self, 'persist_mode', _process_mode)
		object.__setattr__(self, 'flush_mode', _flush_mode)


__all__ = [
	'ProcessArgs'
]