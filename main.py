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

@app.route('/admin/register', methods=['POST'])
def userRegister():
    adminname = request.json.get('adminname')
    password = request.json.get('password')
    telephone = request.json.get('telephone')
    email = request.json.get('email')
    if(adminname == "" or password == ""):
        data = {
            "code": -1,
            "msg": "用户名或密码为空"
        }
    else:
        if(1):#todo getAdminID  判断用户名是否存在
            data = {
                "code": -2,
                "msg": "用户名已存在"
            }
        else:
            password = encryption.getMd5(password)
            # todo 存数据库
            # 获得管理员id
            id = -1
            data = {
                "code": 200,
                "msg": "Success",
                "manageID": id
            }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/admin/login', methods=['POST'])
def userLogin():
    adminname = request.json.get('adminname')
    password = request.json.get('password')
    if(adminname == "" or password == ""):
        data = {
            "code": -1,
            "msg": "用户名或密码为空"
        }
    else:
        myPass = "ccc"  # getAdminPassword(adminname)
        if(encryption.getMd5(password) == myPass):
            ecbObj = encryption.ECBCipher()
            # getUserID()
            # todo 使用id作为token内容
            token = ecbObj.encrypted(adminname+str(int(time.time())+86400))
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
