from pydash import omit
from typing import Any, Union
from uuid import uuid4

# function_decorators:
def staticclass(cls):
    cls.__init__ = _init_handler_for_static_class
    return cls


# helper_functions:
def is_empty(value:Any) -> bool:
    return not (isinstance(value, int) or (isinstance(value, str) and value.strip() != '') or (not isinstance(value, str) and value))

def is_non_negative(val:Any) -> bool:
    return isinstance(val, (int, float)) and val >= 0

def parse_bool(value:Any) -> bool:
    return (isinstance(value, bool) and value) or (isinstance(value, str) and value.lower() == 'true')

def parse_int(num:Any, default=0) -> Union[int, None]:
    return default if num is None else None if not num.isdigit() else int(num)

def uid_gen() -> str:
    return str(uuid4())


# internals:
class CannotInitializeStaticClassError(Exception):
    pass

def _init_handler_for_static_class(*args, **kwargs):
    raise CannotInitializeStaticClassError()


__all__ = [
    'pruned',
    'staticclass',
    'is_empty',
    'is_non_negative',
    'parse_int',
    'prune_keys',
    'uid_gen'
]