# -*- coding: utf-8 -*-
"""
    xeonmpp.server.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 服务端相关数据库ORM
"""

from sqlalchemy import Column, Integer, String, Boolean, Double
from sqlalchemy import ForeignKey  
from sqlalchemy.orm import declarative_base

'''
# ORM 对象
'''
Base = declarative_base()

class User(Base):
    '''用户结构
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)      # 主键 PK
    fd = Column(Integer, default=0)                 # 连接文件描述符，用于消息在线转发
    online = Column(Boolean, default=False)         # 在线状态
    banned = Column(Boolean, default=False)         # 封禁状态
    username = Column(String(16))                   # 用户名，确保唯一（便于登录）
    salt = Column(String(16))                       # 密码盐，确保唯一 为base64编码后的值，原始长度为16/4*3 = 12
    password = Column(String(32))                   # 密码MD5值
    description = Column(String(64),default="This user is lazy, he/she has not written anything yet.")  #个性签名

class Sessions(Base):
    '''用户sesssion
    '''
    __tablename__ = 'sesssion_id'
    sid = Column(Integer, primary_key=True, autoincrement=True)         # 主键 PK
    uid = Column(Integer, ForeignKey("user.id"), default="None")       # 外键 UID
    create_time = Column(Double, default=None)      #session创建时间/时间戳
    keep = Column(Integer, default=3600*24*7)       #session的存在时间/秒
    session = Column(String(36), default="")        #session值
    

class FriendRelation(Base):
    '''朋友关系
    记得去重，避免重复建立关系
    记得检查重复
    '''
    __tablename__ = 'relation_friend'
    rid = Column(Integer, primary_key=True, autoincrement=True)     # 关系ID 主键PK
    uid = Column(Integer, default=0)            # user id
    fid = Column(Integer, default=0)            # friend id


class GroupRelation(Base):
    '''群关系
    '''
    __tablename__ = 'relation_group'
    rid = Column(Integer, primary_key=True, autoincrement=True)     # 关系ID 主键PK
    uid = Column(Integer, default=0)            # user id
    gid = Column(Integer, default=0)            # friend id


class GroupMessage(Base):
    '''群消息 - 一对多
    '''
    __tablename__ = 'message_group'
    id = Column(Integer, primary_key=True, autoincrement=True)      # 主键 PK
    mid = Column(Integer, primary_key=True)     # 消息id message id
    gr_id = Column(Integer, ForeignKey("relation_group.rid"), default=0)  #群关系ID
    message = Column(String(4096),default="")   # 消息

class FriendMessage(Base):
    '''好友消息 - 一对一
    '''
    __tablename__ = 'message_friend'
    id = Column(Integer, primary_key=True, autoincrement=True)      # 主键 PK
    mid = Column(Integer, primary_key=True)     # 消息id message id
    fr_id = Column(Integer, ForeignKey("relation_friend.rid"), default=0)  #好友关系ID
    message = Column(String(4096),default="")   # 消息

class StrangerMessage(Base):
    '''陌生人消息 - 一对一
    带有Warnning
    '''
    __tablename__ = 'message_stranger'
    id = Column(Integer, primary_key=True, autoincrement=True)      # 主键 PK
    mid = Column(Integer, primary_key=True)     # 消息id message id
    from_id = Column(Integer, ForeignKey("user.id"))   #消息来自方的uid
    to_id = Column(Integer, ForeignKey("user.id"))     #消息接受方的uid
    message = Column(String(4096),default="")           #消息

#FEATE OPTIONAL
#日志消息，代码量不够再写

'''
# 序列化 对象
'''
class Package():
    def __init__(self, dest="", to="", type="", data={}) -> None:
        self.dest = dest  # as self.from
        self.to = to
        self.type = type
        self.data = data
    
    
