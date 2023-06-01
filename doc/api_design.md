# API 对接文档
全部使用json格式进行传参，不管是从服务器到客户端还是客户端向服务器传参


## login

- username
- password

  测试账号 

  salt: base64.b64encode(b"123456789012")

  password = md5("aaa").hexdigest() = 47bce5c74f589f4867dbd57e9ca9f808

Request:
```
POST /login HTTP/1.1
Host: 127.0.0.1:5222
Content-Type: application/json
Content-Length: 67

{"username":"test2","password":"47bce5c74f589f4867dbd57e9ca9f808" }
```

Response:
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 102

{'error': False, 'status': True, 'session': 'd9057a59-2f5e-4c8b-96ac-9d2c8687ff93', 'message': '登陆成功'}
```

## register

- username
- password
- description [可选]

Request:

46f94c8de14fb36680850768ff1b7f2a = md5("123qwe")

```
POST /register HTTP/1.1
Host: 127.0.0.1:5222
Content-Type: application/json
Content-Length: 67

{"username":"test7","password":"46f94c8de14fb36680850768ff1b7f2a" }
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 0

{'error': False, 'status': True, 'message': '注册成功'}
```

## logout

- username
- session

Request:

```
POST /logout HTTP/1.1
Host: 127.0.0.1:5222
Content-Type: application/json
Content-Length: 70

{"username":"test2","session":"d9057a59-2f5e-4c8b-96ac-9d2c8687ff93" }
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 0

{'error': False, 'status': True, 'message': '成功登出'}
```

