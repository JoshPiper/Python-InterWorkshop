from functools import partial

from api import BaseAPIService, APIException


class BaseSteamAPIService(BaseAPIService):
    hostname = "api.steampowered.com"
    interface = ''
    key = ''

    defaultVersion = 'v2'
    defaultVerb = 'get'
    autoMethods = {}

    def __init__(self, key):
        self.key = key

    def __init_subclass__(cls, interface=None, **kwargs):
        if interface is None:
            cls.interface = cls.__name__[:-3]

        for method in cls.autoMethods:
            if 'version' not in cls.autoMethods[method]:
                cls.autoMethods[method]['version'] = cls.defaultVersion

            if 'verb' not in cls.autoMethods[method]:
                cls.autoMethods[method]['verb'] = cls.defaultVerb

            args = []
            for i in range(0, len(cls.autoMethods[method]['args'])):
                arg = cls.autoMethods[method]['args'][i]
                if len(arg) == 2:
                    arg = (i, *arg, None)
                elif len(arg) == 3:
                    if isinstance(arg[0], int):
                        arg = (*arg, None)
                    else:
                        arg = (i, *arg)
                args.append(arg)
            cls.autoMethods[method]['args'] = tuple(args)

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
            params)

    def authquery(self, verb, method, query={}, version='v1', params={}):
        if len(query) == 0:
            query = {
                'key': self.key
            }
        else:
            query['key'] = self.key

        return self.query(verb, (method, version), query, params)

    def getarg(self, method, args, kwargs, idx, arg, required, default):
        value = default
        if idx is not None and idx < len(args):
            value = args[idx]
        if arg is not None and arg in kwargs:
            value = kwargs[arg]
        if required and value is None:
            raise APIException("Missing required argument '%s' for '%s'"
                               % (arg, method))
        return (arg, value)

    def getargtobj(self, obj, method, args, kwargs, idx, arg, req, default):
        key, value = self.getarg(method, args, kwargs, idx, arg, req, default)
        if value is not None:
            obj[key] = value

        return obj

    def autoquery(self, method, *args, **kwargs):
        data = self.autoMethods[method]

        query = {}
        fetch = partial(self.getargtobj, query, method, args, kwargs)
        for x in data['args']:
            fetch(*x)

        res = self.authquery(data['verb'], method, query, data['version'])

        if 'datakey' in data:
            returned = res.json()
            if isinstance(data['datakey'], str):
                return returned[data['datakey']]

            for key in data['datakey']:
                returned = returned[key]
            return returned
        else:
            return res.json()