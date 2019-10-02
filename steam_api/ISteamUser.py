from . import BaseSteamAPIService


class ISteamUserAPI(BaseSteamAPIService):
    autoMethods = {
        'CheckAppOwnership': {
            'args': {
                (0, 'steamid', True),
                (1, 'appid', True)
            }
        },
        'GetAppPriceInfo': {
            'args': {
                (0, 'steamid', True),
                (1, 'appids', True)
            },
            'version': 'v1'
        },
        'GetFriendList': {
            'args': {
                (0, 'steamid', True),
                (1, 'relationship', False)
            },
            'version': 'v1'
        }
    }

