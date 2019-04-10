from dataclasses import dataclass, field
from scavenger.api import util
from typing import Any

@util.staticclass
class limits:
    @dataclass(frozen=True)
    class closed:
        minimum: Any
        maximum: Any
        comparator: Any = field(default=None, repr=False)
        def validate(self, value:Any) -> bool:
            if value is None or not isinstance(value, type(self.minimum)):
                return False
            if self.comparator:
                #pylint: disable=no-member
                return self.comparator.le(self.minimum, value) and self.comparator.le(value, self.maximum)
            return self.minimum <= value <= self.maximum
        def __repr__(self):
            return 'limit[{}, {}]'.format(self.minimum, self.maximum)

@util.staticclass
class apps:
    page_limit = limits.closed(1, 5)


__all__ = [
    'apps'
]