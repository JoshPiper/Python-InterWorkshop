from functools import partial

from . import BaseSteamAPIService


class IPublishedFileServiceAPI(BaseSteamAPIService):
    autoMethods = {
        'QueryFiles': {
            'args': (
                ('search_text', True),
                ('appid', True),
                ('cursor', False, '*'),
                ('creator_appid', False),
                ('requiredtags', False),
                ('excludedtags', False),
                ('match_all_tags', False),
                ('required_flags', False),
                ('omitted_flags', False),
                ('child_publishedfileid', False),
                ('return_vote_data', False, False),
                ('return_tags', False, False),
                ('return_kv_tags', False, False),
                ('return_previews', False, True),
                ('return_children', False, True),
                ('return_short_description', False, True),
                ('return_for_sale_data', False, True),
                ('return_metadata', False, False),
            ),
            'version': 'v1',
            'datakey': 'response'
        },
    }
