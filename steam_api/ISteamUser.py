from functools import partial

from . import BaseSteamAPIService


class ISteamUserAPI(BaseSteamAPIService):
    autoMethods = {
        'CheckAppOwnership': {
            'args': (
                (0, 'steamid', True),
                (1, 'appid', True),
            )
        },
        'GetAppPriceInfo': {
            'args': (
                (0, 'steamid', True),
                (1, 'appids', True),
            ),
            'version': 'v1'
        },
        'GetFriendList': {
            'args': (
                ('steamid', True),
                ('relationship', False, None),
            ),
            'version': 'v1',
            'datakey': ('friendslist', 'friends')
        },
        'GetPlayerBans': {
            'args': (
                (0, 'steamids', True),
            ),
            'version': 'v1',
            'datakey': 'players'
        },
        'GetPlayerSummaries': {
            'args': (
                (0, 'steamids', True),
            ),
            'datakey': ('response', 'players')
        },
        'GetPublisherAppOwnership': {
            'args': (
                ('steamid', True),
            ),
            'version': 'v3'
        },
        'GetPublisherAppOwnershipChanges': {
            'args': (
                ('packagerowversion', False, '0'),
                ('cdkeyrowversion', False, '0'),
            ),
            'version': 'v1',
            'datakey': 'ownershipchanges'
        },
        'GetUserGroupList': {
            'args': (
                ('steamid', True),
            ),
            'version': 'v1',
            'datakey': 'response'
        },
        'ResolveVanityURL': {
            'args': (
                ('vanityurl', True),
                ('url_type', False),
            ),
            'version': 'v1',
            'datakey': 'response'
        }
    }

    def GrantPackage(self, *args, **kwargs):
        query = {}
        fetch = partial(self.getargtobj, query, 'GrantPackage', args, kwargs)
        fetch(0, 'steamid', True, None)
        fetch(1, 'packageid', True, None)
        fetch(2, 'ipaddress', True, None)
        fetch(3, 'thirdpartykey', False, None)
        fetch(4, 'thirdpartyappid', 'thirdpartykey' in query, None)

        return self.authquery('post', 'GrantPackage', query)
