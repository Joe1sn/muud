# -*- coding: utf-8 -*-
"""
    XeonMPP.server.server
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 这个文件主要实现用户epoll会话的管理
    提供了一个标准化的epoll模型来管理会话连接
    相关协议
        [RFC 6120][Extensible Messaging and Presence Protocol (XMPP): Core]https://www.rfc-editor.org/rfc/rfc6120
"""
import os
import sys
import json
import ssl
import socket
import select

from configparser import ConfigParser

from rprint import *
# from server.urls import *
from server.serialization import *
from server.utils.epollcontrol import *
from server.routers.socket_router import *
from server.routers.http_router import *


class Server():
    def __init__(self,ip="",port="") -> None:
        self.server_ip = ''
        self.server_port = 0
        self.max_conn = 0
        self.max_buf = 0
        self.reconn = 0
        self.reconn_time = 0
        self.die_out = 0
        self.logdir = ""
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        if not self.read_config():
            error("Config File Fata Error!")
            error("Server Now Exit!")
        else:
            success("Server Now Inited...")

        if ip != "":    self.ip = ip
        if port != "":  self.port = port


    '''读取配置文件
    '''
    def read_config(self) -> bool:
        ret = True
        try:
            conf = ConfigParser()
            conf.read(os.path.join(self.base_dir,"../", "config", "server.conf"), encoding="utf-8")
            self.server_ip = str(conf.get("DEFAULT", "server_ip"))
            self.server_port = int(conf.get("DEFAULT", "server_port"))
            self.max_conn = int(conf.get("DEFAULT", "max_conn"))
            self.max_buf = int(conf.get("DEFAULT", "max_buf"))
            self.reconn = int(conf.get("DEFAULT", "reconn"))
            self.reconn_time = int(conf.get("DEFAULT", "reconn_time"))
            self.die_out = int(conf.get("DEFAULT", "die_out"))
            ret = True
        except Exception as e:
            ret = False
            raise (e)
        return ret

    '''日志记录相关
    '''
    def logs(self) -> None:
        pass

    '''开启服务器
    使用epoll模型处理消息
    '''
    def start_server(self):
        
        banner()
        # 创建TCP套接字并监听端口
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.server_ip, self.server_port))
        server.listen(self.max_conn)

        # 创建epoll对象并注册服务器套接字
        epoll = select.epoll()
        epoll.register(server.fileno(), select.EPOLLIN)
        info("Listening on {}:{}...".format(self.server_ip, self.server_port))
        connections = {}
        requests = {}
        responses = {}
        try:
            while True:
                events = epoll.poll(1)

                for fileno, event in events:
                    if fileno == server.fileno():
                        # 有新连接请求
                        try:
                            connection, address = server.accept()
                            info('Connected:', address)

                            #FIXME
                            # chrome https时会引发阻塞
                            # connection = ssl.wrap_socket(connection, server_side=True, 
                            #         certfile=os.path.join(self.base_dir,"../","config","server.crt"),
                            #         keyfile=os.path.join(self.base_dir,"../","config","server.key"),) #升级为SSL连接
                            connection.setblocking(False)
                            epoll.register(connection.fileno(), select.EPOLLIN)
                            connections[connection.fileno()] = connection
                            requests[connection.fileno()] = b''
                            
                        except Exception as e:
                            error("SSL Handshake ERROR")
                            error(e)
                            connection.close()
                            error("Closed Connection")
                        
                    elif event & select.EPOLLIN:
                        # 有数据可读
                        try:
                            data = connections[fileno].recv(4096)
                            if data:
                                requests[fileno] = data
                                # info(data)
                                # data = json.loads(data)
                                # info(connections)
                                # for fd in connections.keys():
                                #     connections[fd].send(data)
                                # info(connections)
                                # TODO: 消息处理函数
                                # if not (b"HTTP" in data or b"http" in data):      #使用raw socket
                                #     router = RawRouter(epoll, connections, requests, fileno, data)

                            else:
                                name = connections[fileno].getpeername()
                                close_connetion(connections, fileno, epoll)
                                info('Disconnected:', name)

                        except Exception as e:
                            info(e)
                            connections[fileno].close()
                            del connections[fileno]
                            epoll.unregister(fileno)
                            error('Connection Closed Befor Close')
                        # except Exception as e:
                        #     error("Wrong With Event Read")
                        #     error(e)

                    elif event & select.EPOLLOUT:
                        # 有数据可写
                        byteswritten = connections[fileno].send(
                            responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]

                    elif event & select.EPOLLHUP:
                        # 连接已挂起
                        epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
                        del requests[fileno]
                        del responses[fileno]
                        info('Disconnected:',
                             connections[fileno].getpeername())
                        
                # 处理请求并生成响应
                for fileno, data in requests.items():
                    if b"HTTP" in data or b"http" in data:
                        # 解析请求头部
                        http = HTTPRequest(data=data, fileno=fileno, connections=connections)
                        http.show()
                        http_route = HTTPRouter(http)
                        # response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello, world!</h1></body></html>'
                        response = http_route.route()
                        responses[fileno] = response
                        connections[fileno].send(response)
                        name = connections[fileno].getpeername()
                        # close_connetion(connections, fileno, epoll)
                        # info('Disconnected:', name)

                        # 构造响应头部和内容
                        # 清空请求缓冲区
                        response = b''
                        data = b''
                    data = b''
                    requests[fileno] = b''

        except KeyboardInterrupt:
            error('KeyboardInterrupt','Exiting...')
        finally:
            # 关闭服务器套接字和epoll对象
            epoll.unregister(server.fileno())
            epoll.close()
            server.close()