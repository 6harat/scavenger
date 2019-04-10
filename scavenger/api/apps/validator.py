from scavenger.api import props, util
from scavenger.api.definitions import ApiError, Detail, Issue

@util.staticclass
class validator:

    @classmethod
    def detail(cls, func):
        async def execute(request, *args, **kwargs):
            # no validation required
            return await func(request, *args, **kwargs)
        return execute

    @classmethod
    def apps(cls, func):
        async def execute(request, *args, **kwargs):
            err_details = []
            coln_id, catg_id, term = map(lambda v: not util.is_empty(v), (
                request.query.get('coln_id'),
                request.query.get('catg_id'),
                request.query.get('term')
            ))
            if term and any((coln_id, catg_id)):
                err_details.append(Detail.build(
                    Issue.ARGS_NOT_SUPPORTED,
                    field='catg_id, coln_id',
                    scenario='`term` is absent'
                ))
            else:
                # validate coln_id and catg_id amongst the list from ps
                pass

            max_page = util.parse_int(
                request.query.get('max_page'),
                default=props.apps.page_limit.minimum
            )

            if not props.apps.page_limit.validate(max_page):
                err_details.append(Detail.build(
                    Issue.INVALID_PARAMETER_VALUE,
                    field='max_page',
                    expected=props.apps.page_limit
                ))

            if err_details:
                raise ApiError(
                    status=400,
                    details=err_details
                )
            return await func(request, *args, **kwargs)
        return execute
    
    @classmethod
    def similar(cls, func):
        async def execute(request, *args, **kwargs):
            # no validation required
            return await func(request, *args, **kwargs)
        return execute
