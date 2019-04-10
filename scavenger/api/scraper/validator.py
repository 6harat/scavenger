from scavenger.api import props, util
from scavenger.api.definitions import ApiError


@util.staticclass
class validator:
    @classmethod
    def __validate_pid__(cls, request):
        if request.match_info.get('pid') not in request.app['process_map']:
            raise ApiError(404)

    @classmethod
    def flush(cls, func):
        async def execute(request, *args, **kwargs):
            cls.__validate_pid__(request)
            return await func(request, *args, **kwargs)
        return execute

    @classmethod
    def peek(cls, func):
        async def execute(request, *args, **kwargs):
            cls.__validate_pid__(request)
            return await func(request, *args, **kwargs)
        return execute

    @classmethod
    def peek_all(cls, func):
        async def execute(request, *args, **kwargs):
            # no validation required
            return await func(request, *args, **kwargs)
        return execute

    @classmethod
    def start(cls, func):
        async def execute(request, *args, **kwargs):
            # no validation required
            return await func(request, *args, **kwargs)
        return execute

    @classmethod
    def stop(cls, func):
        async def execute(request, *args, **kwargs):
            cls.__validate_pid__(request)
            return await func(request, *args, **kwargs)
        return execute

    @classmethod
    def update(cls, func):
        async def execute(request, *args, **kwargs):
            cls.__validate_pid__(request)
            return await func(request, *args, **kwargs)
        return execute
