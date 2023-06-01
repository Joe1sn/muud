# -*- coding: utf-8 -*-
"""
    xeonmpp.server.utils.socket_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 对socket连接进行解析
"""
import json

from rprint import *
from server.serialization import *
from server.urls import urlpatterns

class RawRequest(object):
    '''对要传参类型进行打包
    将 epoll, connections, requests, fileno, package
    统一打包到request中，便于传参
    '''
    def __init__(self, epoll=None, connections=None, requests="", fileno=0, data="",) -> None:
        self.epoll = epoll
        self.connections = connections
        self.requests = requests
        self.fileno = fileno
        self.data = data
        self.socket = connections[fileno]
        self.package = ""
    
    '''
    socket 功能的简单复用
    '''
    def send(self, *args, **kwargs):
        return self.socket.send(*args, **kwargs)

    def getpeername(self, *args, **kwargs):
        return self.socket.getpeername(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.socket.close(*args, **kwargs)


class RawRouter(object):

    '''对消息处理的函数列表
    用于路由处理
    TODO
    param: connections  : 所有连接
    param: requests     : 所有连接的请求
    param: fileno       : 当前fd序号
    param: data         : 接收到的数据

    return: Bool        : True:   成功转到路由
                          False:  出错
    test data: <stream:stream xmlns="jabber:component:accept" xmlns:stream="http://etherx.jabber.org/streams" to=\'example.com\'>
    '''
    def __init__(self, epoll=None, connections=None, requests="", fileno=0, data=""):
        self.request = RawRequest(epoll, connections, requests, fileno, data)
        self.package = ""

        success("Now router the message")
        success("fd: ", self.request.fileno)
        success("ip: ", self.request.getpeername()[0])
        success("port: ", self.request.getpeername()[1])
        # self.unpack()
    
    '''对序列化对象进行反序列化
    '''
    def unpack(self):
        try:
            self.request.package = json.loads(self.request.data.decode("utf-8"), cls=PackageDecoder)
            act = self.request.package["type"]
            debug = urlpatterns[act](self.request)

            return True
        except Exception as e:
            self.request.send(b"500 Internal Error")
            error("API/Raw socket Error")
            error(e)
            return False