# -*- coding: utf-8 -*-
"""
    xeonmpp.manage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 用于测试、数据库迁移
"""

import argparse

from server.db import engine
from server.models import Base
from rprint import *

def runserver(ip="", port=""):
    """Start a server at the specified port."""
    from server.server import Server
    import select,os,socket
    server = Server(ip, port)
    server.start_server()


def migrate():
    """update all database models"""
    Base.metadata.create_all(engine)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='XeonMPP Loader')
    subparsers = parser.add_subparsers(dest='command')
    
    runserver_parser = subparsers.add_parser('runserver', help='start server')
    runserver_parser.add_argument("-p", "--port", type=int, default=8000, help="port to start the server on")
    runserver_parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="ip to start the server on")
    
    migrate_parser = subparsers.add_parser('migrate', help='migrate database')

    args = parser.parse_args()
    if args.command == 'runserver':
        runserver(args.ip,args.port)
    elif args.command == 'migrate':
        migrate()
    
