from typing import final
from sqlalchemy import Column, String, create_engine, Date, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
from Order import order
import time

conn = mysql.connector.connect(
    user='EasyCharge', password='XKThZNNwdTW7CMyy', database='easycharge')


def connectDB():
    tmp = mysql.connector.connect(
    user='EasyCharge', password='XKThZNNwdTW7CMyy', database='easycharge')
    return tmp



# 创建对象的基类:
Base = declarative_base()

# sqlacodegen mysql+mysqlconnector://EasyCharge:XKThZNNwdTW7CMyy@localhost:3306/easycharge>models.py

# 定义对象:


class Admin(Base):
    __tablename__ = 'Admin'

    id = Column(Integer, primary_key=True)
    adminname = Column(String(20), nullable=False)
    password = Column(String(128), nullable=False)
    telephone = Column(String(50))
    email = Column(String(50))


class ChargeInfo(Base):
    __tablename__ = 'ChargeInfo'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    station_id = Column(Integer, nullable=False)
    start_time = Column(String(255), nullable=False)
    stop_time = Column(String(255), nullable=False)
    charge_capacity = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    create_time = Column(String(255), nullable=False)
    totaltime = Column(Integer, nullable=False)
    capCost = Column(Integer, nullable=False)
    serveCost = Column(Integer, nullable=False)
    mode = Column(Integer, nullable=False)


class ChargeStation(Base):
    __tablename__ = 'ChargeStation'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)


class OrderList(Base):
    __tablename__ = 'OrderList'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    create_time = Column(String(255), nullable=False)
    mode = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    totalCapacity = Column(Integer, nullable=False)


class Statistic(Base):
    __tablename__ = 'Statistics'

    date = Column(Date, primary_key=True)
    station_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    charge_cost = Column(Integer, nullable=False)
    service_cost = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(128), nullable=False)
    telephone = Column(String(50))
    email = Column(String(50))


# 初始化数据库连接:
engine = create_engine(
    'mysql+mysqlconnector://EasyCharge:XKThZNNwdTW7CMyy@localhost:3306/easycharge',pool_size=100)
# 创建DBSession类型: 
DBSession = sessionmaker(bind=engine)


def getUsersNum():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM User;')
    values = cursor.fetchone()
    if not values:
        return 0
    if values[0] == None:
        return 0

    result = values[0]

    return result


def insertUser(tmp_id, tmp_username, tmp_password, tmp_telephone, tmp_email):
    try:
        session = DBSession()
        user = User(
            id=tmp_id,
            username=tmp_username,
            password=tmp_password,
            telephone=tmp_telephone,
            email=tmp_email
        )
        session.add(user)
        session.commit()
        tmp = session.query(User).filter_by(id=tmp_id).first()
        if not tmp:
            return -1
        return 0
    finally:
        session.close()


def updateUser(tmp_id, tmp_username, tmp_password, tmp_telephone, tmp_email):
    try:
        session = DBSession()
        tmp = session.query(User).filter_by(id=tmp_id).first()
        if not tmp:
            return -2
        tmp.username = tmp_username
        tmp.password = tmp_password
        tmp.telephone = tmp_telephone
        tmp.email = tmp_email
        session.commit()
        test = session.query(User).filter_by(id=tmp_id).first()
        if (test.username != tmp_username or test.password != tmp_password or
                test.telephone != tmp_telephone or tmp.email != tmp_email):
            return -1
        return 0
    finally:
        session.close()


def getUserByName(tmp_username):
    try:
        session = DBSession()
        tmp = session.query(User).filter_by(username=tmp_username).first()
        if not tmp:
            return 0
        return tmp.id
    finally:
        session.close


def getAdminByName(tmp_Adminname):
    try:
        session = DBSession()
        tmp = session.query(Admin).filter_by(adminname=tmp_Adminname).first()
        if not tmp:
            return 0
        return tmp.id
    finally:
        session.close()


def insertAdmin(tmp_id, tmp_Adminname, tmp_password, tmp_telephone, tmp_email):
    try:
        session = DBSession()
        admin = Admin(
            id=tmp_id,
            adminname=tmp_Adminname,
            password=tmp_password,
            telephone=tmp_telephone,
            email=tmp_email
        )
        session.add(admin)
        session.commit()
        tmp = session.query(Admin).filter_by(id=tmp_id).first()
        if not tmp:
            return -1
        return 0
    finally:
        session.close()


def getAdminsNum():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM Admin')
    values = cursor.fetchone()
    if not values:
        return 0
    if values[0] == None:
        return 0

    return values[0]


def getUserPassByName(tmp_username):
    try:
        session = DBSession()
        tmp = session.query(User).filter_by(username=tmp_username).first()
        if not tmp:
            return None
        return tmp.password
    finally:
        session.close()


def getAdminPassByName(tmp_adminname):
    try:
        session = DBSession()
        tmp = session.query(Admin).filter_by(adminname=tmp_adminname).first()
        if not tmp:
            return None
        return tmp.password
    finally:
        session.close()


def getUserPassById(tmp_id):
    try:
        session = DBSession()
        tmp = session.query(User).filter_by(id=tmp_id).first()
        if not tmp:
            return None
        return tmp.password
    finally:
        session.close()

def getUserNameById(tmp_id):
    try:
        session = DBSession()
        tmp = session.query(User).filter_by(id=tmp_id).first()
        if not tmp:
            return None
        return tmp.username
    finally:
        session.close()

def getAdminPassById(adminid):
    try:
        session = DBSession()
        tmp = session.query(Admin).filter_by(id=adminid).first()
        if not tmp:
            return None
        return tmp.password
    finally:
        session.close()


def getOrdersNum():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM OrderList')
    values = cursor.fetchone()
    if not values:
        return 0
    if values[0] == None:
        return 0
    return values[0]
#100 80 60 90
#    90 1
#       90

def insertOrder(tmp_id, tmp_userid, tmp_status,  tmp_creatTime, tmp_mode, tmp_capacity, tmp_totalCapacity):
    try:
        intCapacity = int(tmp_capacity * 100)    
        intTotalCapacity = int(tmp_totalCapacity * 100)
        session = DBSession()
        orderlist = OrderList(
            id=tmp_id,
            user_id=tmp_userid,
            status=tmp_status,
            create_time=tmp_creatTime,
            mode=tmp_mode,
            capacity=intCapacity,
            totalCapacity=intTotalCapacity
        )
        session.add(orderlist)
        session.commit()
        tmp = session.query(OrderList).filter_by(id=tmp_id).first()
        if not tmp:
            return -1
        return 0
    finally:
        session.close()


def updateOrder(tmp_id, tmp_userid, tmp_status,  tmp_creatTime, tmp_mode, tmp_capacity, tmp_totalCapacity):
    try:
        session = DBSession()
        tmp = session.query(OrderList).filter_by(id=tmp_id).first()
        if not tmp:
            return -2
        intCapacity = int(tmp_capacity * 100)    
        intTotalCapacity = int(tmp_totalCapacity * 100)
        tmp.user_id = tmp_userid
        tmp.status = tmp_status
        tmp.create_time = tmp_creatTime
        tmp.mode = tmp_mode
        tmp.capacity = intCapacity
        tmp.totalCapacity = intTotalCapacity
        session.commit()
        test = session.query(OrderList).filter_by(id=tmp_id).first()
        if (test.user_id != tmp_userid or test.status != tmp_status or test.create_time != tmp_creatTime or
                test.mode != tmp_mode or test.capacity != intCapacity or test.totalCapacity != intTotalCapacity):
            return -1
        return 0
    finally:
        session.close()

# 将订单状态改为4
# 表示已支付


def setOrderEnd(tmp_id):
    try:
        session = DBSession()
        tmp = session.query(OrderList).filter_by(id=tmp_id).first()
        if not tmp:
            return -2
        tmp.status = 4
        session.commit()
        test = session.query(OrderList).filter_by(id=tmp_id).first()
        if test.status != 4:
            return -1
        return 0
    finally:
        session.close()


def getOrderDetailNum():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM ChargeInfo')
    values = cursor.fetchone()
    if not values:
        return 0
    if values[0] == None:
        return 0

    return values[0]


def updateOrderDetail(tmp_id, tmp_creatTime, tmp_mode, tmp_capacity):
    try:
        intCapacity = int(tmp_capacity * 100) 
        session = DBSession()
        tmp = session.query(ChargeInfo).filter_by(id=tmp_id).first()
        if not tmp:
            return -2
        tmp.create_time = tmp_creatTime
        tmp.mode = tmp_mode
        tmp.charge_capacity = intCapacity
        test = session.query(ChargeInfo).filter_by(id=tmp_id).first()
        if (test.create_time != tmp_creatTime or test.mode != tmp_mode or test.charge_capacity != intCapacity):
            return -1
        return 0
    finally:
        session.close()


def insertOrderDetail(tmp_id, tmp_orderid, tmp_creatTime, tmp_chargeId, tmp_curCap, tmp_totaltime,
                      tmp_startTime, tmp_endTime, tmp_capCost, tmp_serveCost, tmp_cost, tmp_mode):
    try:
        intCapacity = int(tmp_curCap * 100) 
        session = DBSession()
        intcost = int(tmp_cost * 100)
        intScost = int(tmp_serveCost * 100)
        intCcost = int(tmp_capCost * 100)
        chargeinfo = ChargeInfo(
            id=tmp_id,
            order_id=tmp_orderid,
            station_id=tmp_chargeId,
            start_time=tmp_startTime,
            stop_time=tmp_endTime,
            charge_capacity=intCapacity,
            cost=intcost,
            create_time=tmp_creatTime,
            totaltime=tmp_totaltime,
            capCost=intCcost,
            serveCost=intScost,
            mode=tmp_mode
        )
        session.add(chargeinfo)
        session.commit()
        tmp = session.query(ChargeInfo).filter_by(id=tmp_id).first()
        if not tmp:
            return -1
        return 0
    finally:
        session.close()

# 将详单各字段通过字典返回
# {
#     "id": 70,
#     "creatTime": "2004-06-02 11:43:47",
#     "chargeId": 40,
#     "chargeCapacity": 1999,
#     "totaltime": "1986-07-08 PM 18:19:18",
#     "startTime": "1974-08-18 05:43:53",
#     "endTime": "2021-03-14 16:21:05",
#     "capCost": 94,
#     "serveCost": 12,
#     "cost": 37
# }


def getOrderDetailByOrder(tmp_orderid):
    try:
        session = DBSession()
        tmp = session.query(ChargeInfo).filter_by(order_id=tmp_orderid).first()
        if not tmp:
            return None
        floatCapacity = round((float(tmp.charge_capacity) / 100), 2)
        floatCost = round((float(tmp.cost) / 100), 2)
        floatSCost = round((float(tmp.serveCost) / 100), 2)
        floatCCost = round((float(tmp.capCost) / 100), 2)
        orderdict = {
            'id': tmp.id,
            'orderid': tmp.order_id,
            'chargeId': tmp.station_id,
            'startTime': tmp.start_time,
            'endTime': tmp.stop_time,
            'chargeCapacity': floatCapacity,
            'cost': floatCost,
            'creatTime': tmp.create_time,
            'totaltime': tmp.totaltime,
            'capCost': floatCCost,
            'serveCost': floatSCost,
            'mode': tmp.mode
        }
        return orderdict
    finally:
        session.close()


# 传入一个用户id，返回该用户正在进行中的订单id
def getOrderingByUser(userid):
    try:
        session = DBSession()
        tmp = session.query(OrderList).filter(
            OrderList.user_id == userid, OrderList.status != 4, OrderList.status != 5).first()
        if not tmp:
            return None
        return tmp.id
    finally:
        session.close()


# 返回一个order类的对象
# 包含一下五个属性
# id, status, mode, capacity, createTime
# 失败返回None
def getOrderById(orderId):
    try:
        session = DBSession()
        tmp = session.query(OrderList).filter_by(id=orderId).first()
        if not tmp:
            return None
        floatCapacity = round((float(tmp.capacity) / 100), 2)
        result = order(tmp.id, tmp.user_id, tmp.status, tmp.mode, floatCapacity, tmp.create_time)

        return result
    finally:
        session.close()


# 返回用户userid的所有order 返回一个list list中每个元素是一个字典 存储order的信息
def getordersByUser(userid):
    try:
        session = DBSession()
        tmp = session.query(OrderList).filter_by(user_id=userid).all()
        if not tmp:
            return None
        listorder = []
        for row in tmp:
            floatCapacity = round((float(row.capacity) / 100), 2)
            floatTotalCapacity = round((float(row.totalCapacity) / 100), 2)
            orderdict = {
                
                'id': row.id,
                'userid': row.user_id,
                'status': row.status,
                'totalCapacity': floatTotalCapacity,
                'capacity': floatCapacity,
                'creatTime': row.create_time,
                'mode': row.mode
            }
            listorder.append(orderdict)
        return listorder
    finally:
        session.close()


# id为空 表示所有充电桩 否则只选该id充电桩
# 返回选中充电桩时间范围内每一天的的总充电量
# 日期、充电桩编号、累计充电次数、累计充电时长、累计充电量、累计充电费用、累计服务费用、累计总费用
# 返回格式示例
# [
#     {
#         "date": "1974-04-07",
#         "pointID": 99,
#         "chargeTotalCnt": 5,
#         "chargeTotalTime": 1457190363720,
#         "chargeTotalElec": 70,
#         "chargeTotalCcost": 50,
#         "chargeTotalScost": 7,
#         "chargeTotalcost": 12
#     },
#     {
#         "date": "1974-04-08",
#         "pointID": 99,
#         "chargeTotalCnt": 5,
#         "chargeTotalTime": 1457190363720,
#         "chargeTotalElec": 70,
#         "chargeTotalCcost": 50,
#         "chargeTotalScost": 7,
#         "chargeTotalcost": 12
#     }
# ]
def getPointReport(start, end, id):
    try:
        startStruct = time.strptime(start, "%Y-%m-%d")
        startStamp = time.mktime(startStruct)
        endStruct = time.strptime(end, "%Y-%m-%d")
        endStamp = time.mktime(endStruct)
        session = DBSession()
        tmp = session.query(ChargeInfo).all()
        if (id != None):
            tmp = session.query(ChargeInfo).filter_by(station_id=id).all()
        if not tmp:
            return []
        listInfo = []
        for row in tmp:
            tmp_time = row.stop_time
            tmp_struct = time.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")
            tmp_stamp = time.mktime(tmp_struct)
            if (tmp_stamp >= startStamp and tmp_stamp <= endStamp):
                tmp_date = time.strftime("%Y-%m-%d", tmp_struct)
                tmp_staid = row.station_id
                appendflag = True
                for tmpdict in listInfo:
                    if not tmpdict:
                        break
                    if tmpdict['date'] == tmp_date and tmpdict['pointID'] == tmp_staid:
                        floatCapacity = round((float(row.charge_capacity) / 100), 2)
                        floatCost = round((float(row.cost) / 100), 2)
                        floatSCost = round((float(row.serveCost) / 100), 2)
                        floatCCost = round((float(row.capCost) / 100), 2)
                        appendflag = False
                        tmpdict['chargeTotalCnt'] = tmpdict['chargeTotalCnt'] + 1
                        tmpdict['chargeTotalTime'] = tmpdict['chargeTotalTime'] + row.totaltime
                        tmpdict['chargeTotalElec'] = round((tmpdict['chargeTotalElec'] + floatCapacity), 2)
                        tmpdict['chargeTotalCcost'] = round((tmpdict['chargeTotalCcost'] + floatCCost), 2)
                        tmpdict['chargeTotalScost'] = round((tmpdict['chargeTotalScost'] + floatSCost), 2)
                        tmpdict['chargeTotalcost'] = round((tmpdict['chargeTotalcost'] + floatCost), 2)
                        break


                if appendflag:
                    floatCapacity = round((float(row.charge_capacity) / 100), 2)
                    floatCost = round((float(row.cost) / 100), 2)
                    floatSCost = round((float(row.serveCost) / 100), 2)
                    floatCCost = round((float(row.capCost) / 100), 2)
                    orderdict = {
                        "date": tmp_date,
                        "pointID": row.station_id,
                        "chargeTotalCnt": 1,
                        "chargeTotalTime": row.totaltime,
                        "chargeTotalElec": floatCapacity,
                        "chargeTotalCcost": floatCCost,
                        "chargeTotalScost": floatSCost,
                        "chargeTotalcost": floatCost
                    }
                    listInfo.append(orderdict)
        return listInfo
    finally:
        session.close()
