'''
HTTP Response 是服务器返回给客户端的响应，它包含了响应头和响应体两部分。

HTTP Response 的响应头包含了以下信息：

状态行，包括 HTTP 版本、状态码和状态码描述
响应头字段，如 Content-Type、Content-Length、Cache-Control、Location 等，用于描述响应内容的类型、长度、缓存策略、重定向地址等
其他头字段，如 Set-Cookie、Expires、Last-Modified 等，用于描述服务器端的一些信息和配置
HTTP Response 的响应体包含了服务器返回的实际内容，如 HTML、JSON、图片、音频等。响应体的格式和内容根据响应头中的 Content-Type 字段而定。

常见的 HTTP Response 状态码包括：

1xx（信息类）：表示接收到请求并继续处理
2xx（成功）：表示请求已成功被服务器接收、理解、并接受
3xx（重定向）：表示需要客户端采取进一步的操作才能完成请求
4xx（客户端错误）：表示客户端可能出错，如请求格式错误、无权限、资源不存在等
5xx（服务器错误）：表示服务器出错，如服务器崩溃、程序错误等
常见的 HTTP Response 状态码和描述包括：

200 OK：请求成功，服务器已经处理请求并返回数据
201 Created：请求成功，服务器已经创建了新的资源
204 No Content：请求成功，但是响应中没有实体的主体部分
301 Moved Permanently：请求的资源已被永久移动到新 URL
302 Found：请求的资源已被临时移动到新 URL
304 Not Modified：请求的资源未被修改，可以使用缓存的版本
400 Bad Request：请求出现语法错误
401 Unauthorized：未授权，需要用户进行身份验证
403 Forbidden：服务器拒绝请求，没有权限访问
404 Not Found：请求的资源不存在
500 Internal Server Error：服务器出错，不能完成请求
503 Service Unavailable：服务器过载或维护中，暂时无法处理请求
这些状态码和描述是 HTTP Response 的一部分，客户端需要根据实际情况来处理这些响应。
'''
import json

status_code_dict = {
    200:"OK",
    201:"Created",
    204:"No Content",
    301:"Moved Permanently",
    302:"Found",
    304:"Not Modified",
    400:"Bad Request",
    401:"Unauthorized",
    403:"Forbidden",
    404:"Not Found",
    500:"Internal Server Error",
    503:"Service Unavailable",
}
'''
video/mp4：MP4视频
video/mpeg：MPEG视频
application/octet-stream：二进制数据流
'''

content_types = {
    "text": "text/plain",
    "html": "text/html",    #HTML文档
    "css" : "text/css",     #CSS样式表
    "js" : "text/javascript",   #JavaScript脚本

    "json": "application/json",
    "pdf": "application/pdf",
    "xml": "application/xml",
    "bin": "application/octet-stream",  #[特质]

    "jpeg": "image/jpeg",   #JPEG图像
    "png": "image/png",     #PNG图像
    "gif": "image/gif",     #GIF图像

    "mpeg": "audio/mpeg",   #MPEG音频
    "wav": "audio/wav",     #WAV音频

    "mp4" : "video/mp4",    #MP4视频
    "mpeg" : "video/mpeg",  #MPEG视频

    "post_file": "multipart/form-data;"  #文件上传

}

class Response():
    def __init__(self, type="json", status_code=200, 
                        reply="") -> None:
        self.content_type = content_types[type]
        self.status_code = status_code
        if type == "json":
            self.reply = json.dumps(reply, ensure_ascii=False).encode('unicode_escape').decode()
        else:   self.reply = reply
        self.length = len(self.reply)

    def consum(self) -> bytes:
        result = ""
        result += "HTTP/1.1 {status_code} {msg}\r\n".format(
            status_code=self.status_code,   msg=status_code_dict[self.status_code])
        result += "Content-Type: {type}\r\n".format(
            type = self.content_type)
        result += "Content-Length: {length}\r\n".format(
            length=self.length)
        result += "\r\n"

        result = result.encode()
        if type(self.reply) == bytes:
            result += self.reply
        else:   result += self.reply.encode()
        return result
    




# response = "HTTP/1.1 {status_code} {msg}\r\n"   #"HTTP/1.1 200 OK\r\n"
# response += "Content-Type: application/json\r\n"          #"Content-Type: text/html\r\n" 
# response += "Content-Length: {length}\r\n"
# response += "\r\n"
# response += "{json_data}"