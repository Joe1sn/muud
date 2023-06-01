from rprint import *

'''epoll 删除连接
'''
def close_connetion(connections, fileno, epoll):
    try:
        connections[fileno].close()
        del connections[fileno]
        epoll.unregister(fileno)   
    except Exception as e:
        error("Fatal","Can't delete the connection!!!")
        error(e)
        return

def close_request(request):
    try:
        request.connections[request.fileno].close()
        del request.connections[request.fileno]
        request.epoll.unregister(request.fileno)   
    except Exception as e:
        error("Fatal","Can't delete the connection!!!")    
        error(e)
        return