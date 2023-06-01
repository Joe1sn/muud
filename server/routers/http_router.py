# -*- coding: utf-8 -*-
"""
    xeonmpp.server.utils.http_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 对http报文进行解析
"""
import re
import json

from rprint import *
from server.utils.regex import *
from server.urls import urlpatterns

class HTTPRequest(object):
    def __init__(self, data: bytes, fileno: int, connections) -> None:
        self.supported_method = ["GET", "POST"]
        self.raw_data = data
        self.connections = connections
        self.fileno = fileno
        self.headers = []
        self.method = ""
        self.path = ""
        self.query_string = None
        self.data = {}

        if not self.parser():
            error("Invalid HTTP Data")
            return
        if self.method == 'GET':    self.get()
        elif self.method == 'POST': self.post()
        else:
            error("Invaild Method")
            return

    def parser(self) -> bool:
        '''得到关键参数
        '''
        # 解析 HTTP 请求
        try:
            self.method = r_method.search(self.raw_data.decode()).group(1)
            self.path = r_path.search(self.raw_data.decode()).group(1)
            if self.method.upper() not in self.supported_method:
                return False
            return True
        except Exception as e:
            error("Incorrect HTTP Message")
            error(e)
            return False

    def show(self) -> None:
        success(self.method, self.path)
        # info('Method:', self.method)
        # info('Path:', self.path)
        # info('query_string:', self.query_string)
        # info('Data:', self.data)
    
    def post(self):
        '''得到POST参数
        '''
        if self.method == "POST":
            try:
                content_length = int(r_content_length.search(self.raw_data.decode()).group(1))
                content_type = str(r_content_type.search(self.raw_data.decode()).group(1))
                self.query_string = self.raw_data.decode()[-content_length:]
                if "json" in content_type:      #json类型数据
                    self.data = json.loads(self.query_string)
                else:                           #其他普通类型
                    for item in self.query_string.split('&'):
                        key, value = item.split('=')
                        self.data[key] = value
            except Exception as e:
                error(e)
        else:
            error("Incorrect Method, Should be POST")

    def get(self):
        '''得到GET参数
        '''        
        if self.method == "GET":
            self.query_string = r_get_query.search(self.raw_data.decode())

            if self.query_string != None:   
                self.query_string = self.query_string.group(1)
                for item in self.query_string.split('&'):
                    key, value = item.split('=')
                    self.data[key] = value
            else:   self.query_string = None
        else:
            error("Incorrect Method, Should be GET")


class HTTPRouter(object):
    def __init__(self, http_request: HTTPRequest) -> None:
        self.http_request = http_request

    def show(self) -> None:
        success('Method:', self.http_request.method)
        success('Path:', self.http_request.path)
        success('query_string:', self.http_request.query_string)
        success('Data:', self.http_request.data)

    def route(self):
        try:
            ret = urlpatterns[self.http_request.path]
            # return ret(self.http_request)
        except Exception as e:
            error(e)
            ret = urlpatterns["/404"]
        return ret(self.http_request)