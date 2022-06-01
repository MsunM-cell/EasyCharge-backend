import waitArea
import database
import Order
import encryption
import ChargeArea
from asyncio.windows_events import NULL
from contextlib import nullcontext
from distutils.log import debug
from operator import methodcaller
import json
import time
from flask import Flask
from flask import request

app = Flask(__name__)
wait = waitArea.waitingArea()
charging = ChargeArea.chargeArea(wait)


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
        if(database.getUserByName() != 0):
            data = {
                "code": -2,
                "msg": "用户名已存在"
            }
        else:
            password = encryption.getMd5(password)
            id = database.getUsersNum()+1
            database.insertUser(id, username, password, telephone, email)
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
        myPass = database.getUserPassByName(username)
        if(encryption.getMd5(password) == myPass):
            ecbObj = encryption.ECBCipher()
            id = database.getUserByName(username)
            token = ecbObj.encrypted(str(id)+str(int(time.time())+86400))
            if(token == None):
                data = {
                    "code": -2,
                    "msg": "Token生成失败"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "Success",
                    "token": token,
                    "id":id
                }
        else:
            data = {
                "code": -3,
                "msg": "登录失败，请检查用户名或密码是否正确"
            }
        response = json.dumps(data)
        return response, 200, {"Content-Type": "application/json"}


@app.route('/admin/register', methods=['POST'])
def adminRegister():
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
        if(database.getAdminByName(adminname) != 0):
            data = {
                "code": -2,
                "msg": "用户名已存在"
            }
        else:
            password = encryption.getMd5(password)
            id = database.getAdminsNum()+1
            database.insertAdmin(id, adminname, password, telephone, email)
            data = {
                "code": 200,
                "msg": "Success",
                "manageID": id
            }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/admin/login', methods=['POST'])
def adminLogin():
    adminname = request.json.get('adminname')
    password = request.json.get('password')
    if(adminname == "" or password == ""):
        data = {
            "code": -1,
            "msg": "用户名或密码为空"
        }
    else:
        myPass = database.getAdminPassByName(adminname)
        if(encryption.getMd5(password) == myPass):
            ecbObj = encryption.ECBCipher()
            id = database.getAdminByName(adminname)
            token = ecbObj.encrypted(str(id)+str(int(time.time())+86400))
            if(token == None):
                data = {
                    "code": -2,
                    "msg": "Token生成失败"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "Success",
                    "token": token,
                    "id":id
                }
        else:
            data = {
                "code": -3,
                "msg": "登录失败，请检查用户名或密码是否正确"
            }
        response = json.dumps(data)
        return response, 200, {"Content-Type": "application/json"}


@app.route('/users/setInfo', methods=['POST'])
def userSetInfo():
    token = request.json.get('token')
    username = request.json.get('username')
    password = request.json.get('password')
    telephone = request.json.get('telephone')
    email = request.json.get('email')
    result = encryption.tokenDecode(token)
    if(result == None):
        data = {
            "code": -1,
            "msg": "登录信息有误，请退出账号重新登录"
        }
    else:
        if(result['time'] < int(time.time())):
            data = {
                "code": -2,
                "msg": "登录信息已失效，请退出账号重新登录"
            }
        else:
            database.updateUser(
                result['id'], username, password, telephone, email)
            data = {
                "code": 200,
                "msg": "Success"
            }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/users/requestCharge', methods=['POST'])
def requestCharge():
    token = request.json.get('token')
    mode = request.json.get('mode')
    capacity = request.json.get('capacity')
    result = encryption.tokenDecode(token)
    if(result == None):
        data = {
            "code": -1,
            "msg": "登录信息有误，请退出账号重新登录"
        }
    else:
        if(result['time'] < int(time.time())):
            data = {
                "code": -2,
                "msg": "登录信息已失效，请退出账号重新登录"
            }
        else:
            if(wait.haveEmpty(mode)):
                myorder = Order.order(database.getOrdersNum(
                )+1, 0, mode, capacity, time.strftime('%Y-%m-%d %H:%M:%S'))
                if(wait.callin(myorder)):
                    myorder.insert()
                    data = {
                        "code": 200,
                        "msg": "Success",
                        "order": {
                            "id": myorder.id,
                            "status": 0,
                            "create_time": myorder.creatTime,
                            "mode": mode,
                            "capacity": capacity
                        },
                        "queuepos": wait.getQuepos(myorder.id, mode)
                    }
                else:
                    data = {
                        "code": -3,
                        "msg": "等待区已满，请稍后再试"
                    }
            else:
                data = {
                    "code": -3,
                    "msg": "等待区已满，请稍后再试"
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/order/getQueuePos', methods=['GET'])
def getQueuePos():
    token = request.json.get('token')
    orderId = request.json.get('orderId')
    result = encryption.tokenDecode(token)
    if(result == None):
        data = {
            "code": -1,
            "msg": "登录信息有误，请退出账号重新登录"
        }
    else:
        if(result['time'] < int(time.time())):
            data = {
                "code": -2,
                "msg": "登录信息已失效，请退出账号重新登录"
            }
        else:
            order = database.getOrderById(orderId)
            if(order.status == 0):  # 等候区
                pos = wait.getQuepos(order.id, order.mode)
                if(order.mode == 0):
                    data = {
                        "code": 200,
                        "msg": "",
                        "queuepos": "F"+str(pos)
                    }
                else:
                    data = {
                        "code": 200,
                        "msg": "",
                        "queuepos": "T"+str(pos)
                    }
            else:
                data = {
                    "code": -1,
                    "msg": "当前订单非等候区状态"
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/order/getFrontCarNum', methods=['GET'])
def getFrontCarNum():
    token = request.json.get('token')
    orderId = request.json.get('orderId')
    result = encryption.tokenDecode(token)
    if(result == None):
        data = {
            "code": -1,
            "msg": "登录信息有误，请退出账号重新登录"
        }
    else:
        if(result['time'] < int(time.time())):
            data = {
                "code": -2,
                "msg": "登录信息已失效，请退出账号重新登录"
            }
        else:
            order = database.getOrderById(orderId)
            if(order.status == 0):  # 等候区
                pos = charging.getModeNum(
                    order.mode)+wait.getQuepos(order.id, order.mode)-1
                data = {
                    "code": 200,
                    "msg": "",
                    "num": pos
                }
            elif(order.status == 1):  # 排队中
                data = {
                    "code": 200,
                    "msg": "",
                    "num": 1
                }
            else:
                data = {
                    "code": -1,
                    "msg": "当前订单非排队状态"
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}


@app.route('/admin/onChargePoint', methods=['POST'])
def onChargePoint():
    token = request.json.get('token')
    pointId = request.json.get('pointId')
    result = encryption.tokenDecode(token)
    if(result == None):
        data = {
            "code": -1,
            "msg": "登录信息有误，请退出账号重新登录"
        }
    else:
        if(result['time'] < int(time.time())):
            data = {
                "code": -2,
                "msg": "登录信息已失效，请退出账号重新登录"
            }
        else:
            if(charging.openCharge(pointId)):
                data = {
                    "code": 200,
                    "msg": "",
                }
            else:
                data = {
                    "code": -1,
                    "msg": "充电桩不存在",
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/admin/closeChargePoint', methods=['POST'])
def closeChargePoint():
    token = request.json.get('token')
    pointId = request.json.get('pointId')
    result = encryption.tokenDecode(token)
    if(result == None):
        data = {
            "code": -1,
            "msg": "登录信息有误，请退出账号重新登录"
        }
    else:
        if(result['time'] < int(time.time())):
            data = {
                "code": -2,
                "msg": "登录信息已失效，请退出账号重新登录"
            }
        else:
            if(charging.closeCharge(pointId)):
                data = {
                    "code": 200,
                    "msg": "",
                }
            else:
                data = {
                    "code": -1,
                    "msg": "充电桩不存在",
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

if __name__ == '__main__':
    app.run(debug=True)  # 运行app
