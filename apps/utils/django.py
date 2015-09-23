#-*- coding: utf-8 -*-

from apps.utils.request_context import RequestContext

class DjangoRequestContext(RequestContext):
    def __init__(self, django_request):
        super(DjangoRequestContext, self).__init__()
        self._request = django_request
        self._params = None
        self._cookies = None
        self._headers = None
    
    @property
    def params(self):
        if self._params is None:
            self._params = dict(self._request.REQUEST.iteritems())
        return self._params
    
    def get_parameter(self, name, default=None):
        return self.params.get(name, default)
    
    @property
    def cookies(self):
        if self._cookies is None:
            self._cookies = self._request.COOKIES
        
        return self._cookies
    
    def get_cookie(self, name, default=None):
        return self.cookies.get(name, default)
    
    @property
    def headers(self):
        if self._headers is None:
            self._headers = self._request.META
        
        return self._headers
    
    def get_header(self, name, default=None):
        return self.headers.get(name, default)
    
    @property
    def path(self):
        return self._request.path
    
    @property
    def query_string(self):
        return self.headers.get('QUERY_STRING')
    
    def get_host(self):
        return self._request.get_host()
    
    def get_http_method(self):
        return self._request.method
    
    @property
    def raw_request(self):
        return self._request
