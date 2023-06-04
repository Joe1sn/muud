import re
# 验证 HTTP 请求报文
r_request = re.compile(rb'^([A-Z]+)\s+([\w/\.]+)\s+HTTP/(\d+\.\d+)\r\n'
                           rb'((?:[\w-]+:.*\r\n)*)(?:\r\n)?'
                           rb'([\s\S]*)$')

# 验证 HTTP 响应报文
r_response = re.compile(rb'^HTTP/(\d+\.\d+)\s+(\d+)\s+([\w\s]+)\r\n'
                            rb'((?:[\w-]+:.*\r\n)*)(?:\r\n)?'
                            rb'([\s\S]*)$')

# 得到 HTTP 报文中的method
r_method = re.compile(rb'([A-Z]+) /')

# 得到 HTTP 报文中的路径
r_path = re.compile(rb'[A-Z]+\s(/[^?\s]*)')

# 得到 HTTP 报文中的GET参数
r_get_query = re.compile(r'\?(.*) HTTP')


# 得到 HTTP 报文中的content_length
r_content_length = re.compile(rb'Content-Length: (\d+)')

# 得到 HTTP 报文中的content_type
r_content_type = re.compile(rb"Content-Type: ([^;]+)")

# 得到 HTTP 报文中的session_od
r_session_id = re.compile(rb'session_id=([^;]+)')

# 得到 HTTP 报文中的文件上传时的boundary值
r_boundary = re.compile(rb"boundary=([^;\r\n$]+)")


'''
# 测试 HTTP 请求报文
request_str = 'GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n'
request_match = request_regex.match(request_str)
if request_match:
    print('Request Method:', request_match.group(1))
    print('Request URI:', request_match.group(2))
    print('HTTP Version:', request_match.group(3))
    print('Headers:\n', request_match.group(4))
    print('Body:\n', request_match.group(5))
else:
    print('Invalid Request')

# 测试 HTTP 响应报文
response_str = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!'
response_match = response_regex.match(response_str)
if response_match:
    print('HTTP Version:', response_match.group(1))
    print('Status Code:', response_match.group(2))
    print('Reason Phrase:', response_match.group(3))
    print('Headers:\n', response_match.group(4))
    print('Body:\n', response_match.group(5))
else:
    print('Invalid Response')
'''