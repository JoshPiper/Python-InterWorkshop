from functools import partial

from api import BaseAPIService, APIException


class BaseSteamAPIService(BaseAPIService):
    hostname = "api.steampowered.com"
    interface = ''
    key = ''

    autoMethods = {}

    def __init__(self, key):
        self.key = key

    def __init_subclass__(cls, interface=None, **kwargs):
        if interface is None:
            cls.interface = cls.__name__[:-3]

    def __getattr__(self, item):
        if item in self.autoMethods:
            return partial(self.autoquery, item)
        else:
            try:
                res = super().__getattr__(item)
                if res is not None:
                    return res
            except APIException:
                raise AttributeError(
                    "'%s' object has no attribute '%s'"
                    % (type(self).__name__, item)
                )

    def build(self, method, query={}, version='v1', params={}):
        return super().build(
            '/'.join((self.interface, *method)),
            query,
            params
    )

    def authquery(self, verb, method, query={}, version='v1', params={}):
        if len(query) == 0:
            query = {
                'key': self.key
            }
        else:
            query['key'] = self.key

        return self.query(verb, (method, version), query, params)

    def autoquery(self, method, *args, **kwargs):
        data = self.autoMethods[method]
        query = {}

        for idx, arg, req in data['args']:
            print(idx, arg, req)
            value = None
            if idx is not None and idx in args:
                value = args[idx]
            if arg is not None and arg in kwargs:
                value = kwargs[arg]
            if req and value is None:
                raise APIException("Missing required argument '%s' for '%s'"
                                   % (arg, method))
            query[arg] = value

        version = 'v2'
        if 'version' in data:
            version = data['version']

        verb = 'get'
        if 'type' in data:
            verb = data['type']

        res = self.authquery(verb, method, query, version)
        if res.status_code == 403:
            raise APIException('Status Code 403 returned. Check API key.')

        return res.json()