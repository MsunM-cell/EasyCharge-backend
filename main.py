import encryption
from asyncio.windows_events import NULL
from contextlib import nullcontext
from distutils.log import debug
from operator import methodcaller
import json
import time
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/users/register', methods=['POST'])
def userRegister():
    username = request.json.get('username')
    password = request.json.get('password')
    telephone = request.json.get('telephone')
    email = request.json.get('email')
    if(username == "" or password == ""):
        data = {
            "code": -1,
            "msg": "用户名或密码为空"
        }
    else:
        password = encryption.getMd5(password)
        # todo 存数据库
        # 获得用户id
        id = -1
        data = {
            "code": 200,
            "msg": "Success",
            "id": id
        }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/users/login', methods=['POST'])
def userLogin():
    username = request.json.get('username')
    password = request.json.get('password')
    if(username == "" or password == ""):
        data = {
            "code": -1,
            "msg": "用户名或密码为空"
        }
    else:
        myPass = "ccc"  # getPassword(username)
        if(encryption.getMd5(password) == myPass):
            ecbObj = encryption.ECBCipher()
            # getUserID()
            # todo 使用id作为token内容
            token = ecbObj.encrypted(username+str(int(time.time())+86400))
            if(token == None):
                data = {
                    "code": -2,
                    "msg": "Token生成失败"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "Success",
                    "token": token
                }
        else:
            data = {
                "code": -3,
                "msg": "登录失败，请检查用户名或密码是否正确"
            }
        response = json.dumps(data)
        return response, 200, {"Content-Type": "application/json"}

    
if __name__ == '__main__':
    app.run(debug=True)  # 运行app
