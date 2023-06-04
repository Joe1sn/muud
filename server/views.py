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
# from server.routers.http_router import HTTPRequest as request

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
# @socket_api
# def socket_auth(request):
#     username = request.package["data"]["user"]
#     password = request.package["data"]["passwd"]
    
#     refresh_db()
#     ret = session.query(User).filter(User.username == username, User.password == password).first()

#     if ret == None:
#         request.send(b"Failed")
#         name = request.getpeername()
#         close_connetion(request.connections, request.fileno, request.epoll)
#         info('Authentication Error', name)
#         return False
#     else:
#         ret = session.query(User).filter(User.id == ret.id).\
#             update({User.online:True})
#         # ret.update({User.online:True})    #报错确认
#         session.commit()           #确认更改
#         request.send(b"True")
#         return True
    
    
# @socket_api
# def sendall_msg(request):
#     # {dest="joe1sn", to="joe1sn@example.com",type="auth", data={"user": "joe1sn","passwd": "xxxx"}}
#     msg = request.package["data"]["msg"]


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
    return result.consum()

@http_api
def html_test(http_request):
    data = "<html><body><h1>Hello, world!</h1></body></html>"
    result = Response(reply=data,type="html")
    return result.consum()

@http_api
def page_404(http_request):
    data = "<html><body><h1>404, Page Not Found</h1></body></html>"
    result = Response(reply=data,type="html",status_code=404)
    return result.consum()

@http_api
def file_test(http_request):
    result=""
    with open(r"/mnt/d/Github/muud/test/test.pdf","rb") as f:
        result = f.read()
    result = Response(reply=result,type="pdf")
    return result.consum()

@http_api
def post_test(http_request):
    result = ""
    for key in http_request.data.keys():
        result += str(key) + " : " + http_request.data[key] + "\n"

    result += "method : " +  http_request.method        
    result = Response(reply=result,type="text")
    return result.consum()

@http_api
def get_test(http_request):
    result = ""
    for key in http_request.data.keys():
        result += str(key) + " : " + http_request.data[key] + "\n"
    result += "method : " +  http_request.method
    result = Response(reply=result,type="text")
    return result.consum()

@http_api
def file_upload(http_request):
    result=""
    with open(r"/mnt/d/Github/muud/test/file_upload.html","rb") as f:
        result = f.read()
    result = Response(reply=result,type="html")
    return result.consum()

@http_api
def upload(http_request):
    result=""
    info("FILE Content>>>>>>>>>")
    # info(http_request.data["len"]/1024,"KB")
    name = http_request.data["filename"]
    # print(http_request.data["file"][:0x20])
    with open(r"/mnt/d/Github/muud/test/"+name,"wb") as f:
        result = f.write(http_request.data["file"])
    data = "<html><body><h1>okok</h1></body></html>"
    result = Response(reply=data,type="html",status_code=200)
    return result.consum()
