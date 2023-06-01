# -*- coding: utf-8 -*-
"""
    xeonmpp.server.views
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ API接口的实现
"""
import time

from hashlib import md5
from sqlalchemy import and_

from rprint import *
from server.models import *
from server.db import session
from server.utils.epollcontrol import *
from server.utils.http_response import *

'''API装饰器部分
'''
def socket_api(func,):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            error("Fatal Error In API")
            error(e)
            close_request(*args, **kwargs)
            return
    return wrapper

def http_api(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            error("Fatal Error In API")
            error(e)
            # close_request(*args, **kwargs)
            return
    return wrapper

'''刷新数据库'''
def refresh_db():
    session.expire_all()       #每次查询刷新所有 ORM对象
    session.commit()           #确认刷新 

'''socket的API
socket_auth: 使用socket的认证机制

'''
@socket_api
def socket_auth(request):
    username = request.package["data"]["user"]
    password = request.package["data"]["passwd"]
    
    refresh_db()
    ret = session.query(User).filter(User.username == username, User.password == password).first()

    if ret == None:
        request.send(b"Failed")
        name = request.getpeername()
        close_connetion(request.connections, request.fileno, request.epoll)
        info('Authentication Error', name)
        return False
    else:
        ret = session.query(User).filter(User.id == ret.id).\
            update({User.online:True})
        # ret.update({User.online:True})    #报错确认
        session.commit()           #确认更改
        request.send(b"True")
        return True
    
    
@socket_api
def sendall_msg(request):
    # {dest="joe1sn", to="joe1sn@example.com",type="auth", data={"user": "joe1sn","passwd": "xxxx"}}
    msg = request.package["data"]["msg"]


#======================================================================================

'''HTTP的API
login   : 客户端登录接口
register: 客户端用户注册接口
'''
def is_login(uid, session_id):
    #session检查
    ret = session.query(Sessions).filter(Sessions.session == session_id, Sessions.uid == uid).first()
    if ret == None: return False
    elif int(time.time()) - ret.create_time > ret.keep:  #超时，删除session
        session.query(Sessions).filter(Sessions.sid == ret.sid).delete()
        return False
    return True

#---- 测试 ----
@http_api
def test(http_request):
    data = str({
            "error": False,
            "status": False,
            "message":"Test Fine"})
    # data = json.dumps(json_data, ensure_ascii=False).encode('unicode_escape').decode()
    result = Response(reply=data)
    return result.consum().encode()

@http_api
def html_test(http_request):
    data = "<html><body><h1>Hello, world!</h1></body></html>"
    result = Response(reply=data,type="html")
    return result.consum().encode()

@http_api
def page_404(http_request):
    data = "<html><body><h1>404, Page Not Found</h1></body></html>"
    result = Response(reply=data,type="html",status_code=404)
    return result.consum().encode()

# #---- 登录 ----
# @http_api
# def login(http_request): #HTTPRequest
#     '''登录
#     测试账号 
#     salt: base64("123456789012")
#     password = md5("aaa") = 47bce5c74f589f4867dbd57e9ca9f808
#     '''
#     result = response
#     json_data = ""
#     data = ""
#     try:  
#         username = http_request.data["username"]
#         passwd = http_request.data["password"]
#         pass_len = len(passwd)
#         if "session" in http_request.data.keys():
#             session_=http_request.data["session"]
#         else:   session_ = ""


#     except:
#         json_data = str({
#                 "error": True,
#                 "status": False,
#                 "message":"参数错误"})
#         data = json.dumps(json_data, ensure_ascii=False).encode('unicode_escape').decode()
#         result = result.format(
#             status_code=200, msg = status_code_dict[200],
#             length = len(data),    json_data = data)
#         return result.encode()
#     try:
#         refresh_db()
#         ret = session.query(User).filter(User.username == username).first()
#     except Exception as e:
#         error(e)
#         result = result.format(
#             status_code=500, msg = status_code_dict[500],
#             length = 0,    json_data = "")
#         return result.encode()
    
#     try:
#         if ret == None or \
#             md5(base64.b64decode(ret.salt)+passwd.encode()).hexdigest() != ret.password:
#             json_data = str({
#                 "error": False,
#                 "status": False,
#                 "message":"用户名或密码错误"})
        
#         elif is_login(ret.id, session_) or session.query(User).filter(and_(User.id == ret.id, User.online == True)).first() != None:
#             json_data = str({
#                 "error": False,
#                 "status": False,
#                 "message":"重复登陆!"})
#         else:
#             session_id = str(uuid.uuid4())
#             session.query(User).filter(User.id == ret.id).\
#                 update({User.online:True, User.fd:http_request.fileno})                     
#             #添加session
#             session_ = Sessions(uid=ret.id, create_time=time.time(), session=session_id)
#             session.add(session_)
#             session.commit()
#             # ret.update({User.online:True})    #报错确认
#             json_data = str({
#                 "error": False,
#                 "status": True,
#                 "session": session_id,
#                 "message":"登陆成功"})
        
#         data = json.dumps(json_data, ensure_ascii=False).encode('unicode_escape').decode()
#         result = result.format(
#             status_code=200, msg = status_code_dict[200],
#             length = len(data),    json_data = data)
#     except Exception as e:
#         error(e)
#         result = result.format(
#             status_code=500, msg = status_code_dict[500],
#             length = 0,    json_data = "")
        
#     return result.encode()

# #---- 登出 ----
# @http_api
# def logout(http_request): #HTTPRequest
#     result = response
#     json_data = ""
#     username = ""
#     data = ""
#     session_ = ""
#     try:  
#         username = http_request.data["username"]
#         session_=http_request.data["session"]
#         ret = session.query(User).filter(User.username == username).first()
#         if not is_login(uid=ret.id, session_id= session_):
#             info(is_login(uid=ret.id, session_id= session_))

#             json_data = str({
#                 "error": False,
#                 "status": False,
#                 "message":"用户未登录"})
#         else:
#             session.query(Sessions).filter(Sessions.session == session_).delete()
#             session.query(User).filter(User.id == ret.id).\
#                 update({User.online:False, User.fd:0})
#             session.commit()
#             json_data = str({
#                 "error": False,
#                 "status": True,
#                 "message":"成功登出"})
#     except Exception as e:
#         error(e)
#         json_data = str({
#                 "error": False,
#                 "status": False,
#                 "message":"参数错误"})
#     data = json.dumps(json_data, ensure_ascii=False).encode('unicode_escape').decode()
#     result = result.format(
#         status_code=200, msg = status_code_dict[200],
#         length = len(data),    json_data = data)
#     return result.encode()

# #---- 注册 ----
# @http_api
# def register(http_request): #HTTPRequest
#     '''用户注册
#     '''
#     result = response
#     json_data = ""
#     data = ""
#     try:
#         username = http_request.data["username"]
#         passwd = http_request.data["password"]
#         if "description" in http_request.data.keys():
#             description=http_request.data["description"]
#         else:   description = False

#         if len(passwd) != 32:
#             json_data = str({
#                 "error": False,
#                 "status": False,
#                 "message":"密码长度出，数据包可能被篡改"})
#             data = json.dumps(json_data, ensure_ascii=False).encode('unicode_escape').decode()
#             result = result.format(
#             status_code=400, msg = status_code_dict[400],
#             length = len(data),    json_data = data)
#             return result.encode()

#         #登录，查询用户名和密码
#         refresh_db()
#         ret = session.query(User).filter(User.username == username).first()
#         if ret != None:
#             json_data = str({
#                 "error": False,
#                 "status": False,
#                 "message":"用户名重复"})
#         else:
#             import random
#             salt =[random.randint(0x00,0xff) for i in range(12)]
#             passwd = md5(bytes(salt)+passwd.encode()).hexdigest()
#             salt = base64.b64encode(bytes(salt))
#             if description:
#                 u = User(username=username,salt=salt, password=passwd, description=description)
#             else:
#                 u = User(username=username,salt=salt, password=passwd)
#             session.add(u)
#             session.commit()
#             json_data = str({
#                 "error": False,
#                 "status": True,
#                 "message":"注册成功"})
#         data = json.dumps(json_data, ensure_ascii=False).encode('unicode_escape').decode()
#         result = result.format(
#             status_code=200, msg = status_code_dict[200],
#             length = len(data),    json_data = data)                      
#     except Exception as e:
#         error(e)
#         result = result.format(
#             status_code=500, msg = status_code_dict[500],
#             length = 0,    json_data = "")
#     return result.encode()


# #---- 消息测试 ---
# @http_api
# def msg(http_request, *args, **kwargs):
#     #从数据库中选择所有在线用户
#     # refresh_db()
#     # users = session.query(User).filter(User.online == True).all()
#     # fd_list = [user.fd for user in users]
#     # info(fd_list)
#     # try:
#     #     msg = http_request.data["msg"]
#     #     for fd in fd_list:
#     #         # if fd != http_request.fileno:
#     #         info("sending message")
#     #         http_request.connections[fd].send(msg.encode())
        
#     # except Exception as e:
#     #     error(e)
#     return b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello, world!</h1></body></html>'







