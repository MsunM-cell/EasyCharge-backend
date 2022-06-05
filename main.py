import waitArea
import database
import Order
import encryption
import ChargeArea
import json
import time
from flask import Flask
from flask import request
from gevent import pywsgi
 

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
        if(database.getUserByName(username) != 0):
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
                    "id":id,
                    "orderId":database.getOrderingByUser(id)
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


@app.route('/order/requestCharge', methods=['POST'])
def requestCharge():
    token = request.json.get('token')
    mode = request.json.get('mode')
    capacity = request.json.get('capacity')
    totalCapacity=request.json.get('totalCapacity')
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
                )+1,int(result['id']), 0, mode, capacity, time.strftime('%Y-%m-%d %H:%M:%S'),totalCapacity)
                if(wait.callin(myorder)):
                    myorder.insert()
                    if(myorder.mode==0):
                        quepos="F"+str(wait.getQuepos(myorder.id, mode))
                    else:
                        quepos="T"+str(wait.getQuepos(myorder.id, mode))
                    data = {
                        "code": 200,
                        "msg": "Success",
                        "order": {
                            "id": myorder.id,
                            "status": 0,
                            "create_time": myorder.createTime,
                            "mode": mode,
                            "capacity": capacity
                        },
                        "queuepos": quepos
                    }
                else:
                    data = {
                        "code": -3,
                        "msg": "等待区已满，请稍后再试"
                    }
            else:
                data = {
                    "code": -4,
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

@app.route('/orders/<int:id>', methods=['GET'])
def getOrder(id):
    token = request.json.get('token')
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
            order = database.getOrderById(id)
            if(order == None):  # 等候区
                data = {
                    "code": -1,
                    "msg": "数据库中未查找到该订单信息"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "",
                    "order":order.json()
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders/details/<int:id>', methods=['GET'])
def getOrderDetails(id):
    token = request.json.get('token')
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
            orderDetail = database.getOrderDetailByOrder(id)
            if(orderDetail == None):  # 等候区
                data = {
                    "code": -1,
                    "msg": "数据库中未查找到该订单信息"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "",
                    "order_detail":orderDetail
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders/charge/<int:id>', methods=['GET'])
def getChargingInfo(id):
    token = request.json.get('token')
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
            chargeInfo=charging.getChargingInfo(id)
            if(chargeInfo == None):  # 等候区
                data = {
                    "code": -1,
                    "msg": "未查找到该订单信息"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "",
                    "charge":chargeInfo
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders/mode/<int:id>', methods=['PUT'])
def putMode(id):
    token = request.json.get('token')
    mode=request.json.get('mode')
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
            flag=wait.setMode(id,mode)
            if(flag == False): 
                data = {
                    "code": -1,
                    "msg": "未查找到该订单信息"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "",
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders/capacity/<int:id>', methods=['PUT'])
def putCapacity(id):
    token = request.json.get('token')
    capacity=request.json.get('capacity')
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
            flag=wait.setCapacity(id,capacity)
            if(flag == None):  
                data = {
                    "code": -1,
                    "msg": "未查找到该订单信息"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "",
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders', methods=['GET'])
def getorders():
    token = request.json.get('token')
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
            List=database.getordersByUser(result['id'])
            if(List!=None):
                data = {
                    "code": 200,
                    "msg": "",
                    "data":List
                }
            else:
                data = {
                    "code": -3,
                    "msg": "信息获取失败"
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders/cancel/<int:id>', methods=['PUT'])
def cancleOrder(id):
    token = request.json.get('token')
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
            order=charging.cancel(id)
            if(order == None):  
                data = {
                    "code": -1,
                    "msg": "未查找到该订单信息"
                }
            else:
                data = {
                    "code": 200,
                    "msg": "",
                    "order":order
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/orders/pay/<int:id>', methods=['PUT'])
def putPay(id):
    token = request.json.get('token')
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
            database.setOrderEnd(id)
            order=database.getOrderById(id).json()
            orderDetail=database.getOrderDetailByOrder(id)
            data = {
                "code": 200,
                "msg": "",
                "order":order,
                "charge_info":orderDetail
            }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/admin/getChargePoint', methods=['GET'])
def getChargePoint():
    token = request.json.get('token')
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
            List=charging.getAllPoints()
            if(List!=None):
                data = {
                    "code": 200,
                    "msg": "",
                    "points":List
                }
            else:
                data = {
                    "code": -3,
                    "msg": "信息获取失败"
                }
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}

@app.route('/admin/getChargePointCar', methods=['GET'])
def getChargePointCar():
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
            result=charging.getWaitInfo(pointId)
            if(result!=None):
                data = {
                    "code": 200,
                    "msg": "",
                    "data":result
                }
            else:
                data = {
                    "code": -3,
                    "msg": "信息获取失败"
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


@app.route('/admin/getPointChargeReport', methods=['GET'])
def getPointChargeReport():
    token = request.json.get('token')
    start = request.json.get('start')
    end = request.json.get('end')
    id = request.json.get('pointId')
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
            result=database.getPointReport(start,end,id)
            if(result!=None):
                data = {
                    "code": 200,
                    "msg": "",
                    "data":result
                }
            else:
                data = {
                    "code": -3,
                    "msg": "信息获取失败"
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

@app.route('/admin/setPointError', methods=['POST'])
def setPointError():
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
            if(charging.setChargeError(pointId)):
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


@app.route('/admin/setPointOK', methods=['POST'])
def setPointOK():
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
            if(charging.setChargeOK(pointId)):
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



# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)  # 运行app


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()