# -*- coding:utf-8 -*-


class RequestContext(object):
    def __init__(self):
        self._data = {}
        self._result = {}

    @property
    def data(self):
        """用于存储handler链处理过程中的临时数据"""
        return self._data

    @property
    def result(self):
        """返回给web层的数据"""
        return self._result

    @property
    def params(self):
        raise NotImplementedError

    def get_parameter(self, name, default=None):
        raise NotImplementedError

    @property
    def cookies(self):
        raise NotImplementedError

    def get_cookie(self, name, default=None):
        raise NotImplementedError

    @property
    def headers(self):
        raise NotImplementedError

    def get_header(self, name, default=None):
        raise NotImplementedError

    @property
    def path(self):
        raise NotImplementedError

    @property
    def query_string(self):
        raise NotImplementedError

    def get_host(self):
        raise NotImplementedError

    def get_http_method(self):
        raise NotImplementedError

    @property
    def raw_request(self):
        raise NotImplementedError