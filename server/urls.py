# -*- coding: utf-8 -*-
"""
    xeonmpp.server.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 路由导航
"""

from server import views as server_api

urlpatterns = {
    # 'auth': server_api.socket_auth,
    '/': server_api.test,
    '/test': server_api.test,
    # '/login': server_api.login,
    # "/register": server_api.register,
    # "/logout": server_api.logout,
    # "/msg": server_api.msg,
    "/html_test": server_api.html_test,
    "/json_test": server_api.test,
    "/404": server_api.page_404,
    "/file_test": server_api.file_test,
}