# -*- coding: utf-8 -*-
"""
    XeonMPP.server.db
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 用于数据库对象的ORM
"""
import os

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from configparser import ConfigParser

class ConnDB:

    def __init__(self) -> None:
        self.__type = ""
        self.__ip = ""
        self.__port = ""
        self.__user = ""
        self.__password = ""
        self.__db = ""
        self.__engine = "pymysql"
        self.connect_db()
        self.__session = sessionmaker(bind=self.__engine)

    def connect_db(self):
        ret = False
        try:
            conf = ConfigParser()
            base = os.path.abspath(os.path.dirname(__file__))
            conf.read(os.path.join(base, "../", "config", "database.conf"), encoding="utf-8")
            self.__type = str(conf.get("conndb", "type"))
            self.__user = str(conf.get("conndb", "user"))
            self.__password = str(conf.get("conndb", "password"))
            self.__ip = str(conf.get("conndb", "ip"))
            self.__port = int(conf.get("conndb", "port"))
            self.__db = str(conf.get("conndb", "db"))
            ret = True
        except Exception as e:
            ret = False
            raise (e)

        # 合成连接语句
        conn_str = '{type}+pymysql://{user}:{password}@{ip}:{port}/{db}'.format(
            type=self.__type, user=self.__user, password=self.__password,
            ip=self.__ip, port=self.__port, db=self.__db
        )

        if ret == True:
            self.__engine = create_engine(conn_str, echo=False)
        else:
            self.__engine = ""
    
    def get_engine(self):
        return self.__engine

    def get_session(self):
        return self.__session


conn_db = ConnDB()
engine = conn_db.get_engine()
Session = conn_db.get_session()
session = Session()