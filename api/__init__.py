from urllib.parse import urlunparse, urlencode
from requests import request
from functools import partial


class APIException(Exception):
    pass


class BaseAPIService:
    scheme = "https"
    hostname = "localhost"
    port = 443
    methods = ['get', 'post', 'head', 'put', 'delete', 'options']

    def host(self):
        if self.port is None:
            return self.hostname
        elif (self.scheme == "https" and self.port != 443 or
              self.scheme == "http" and self.port != 80):
            return "%s:%s" % (self.hostname, self.port)
        else:
            return self.hostname

    def build(self, path, query={}, params={}):
        return urlunparse(
            (self.scheme, self.host(), path, urlencode(params), urlencode(query), '')
        )

    def query(self, method, path, query={}, params={}):
        return request(method, self.build(path, query, params))

    def authquery(self, method, path, query={}, params={}):
        return query(self, method, path, query, params)

    def __getattr__(self, item):
        if item in self.methods:
            return partial(self.query, item)
        else:
            raise APIException("Bad method requested.")

    def __call__(self, *args, **kwargs):
        return self.get(*args)