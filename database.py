from sqlalchemy import Column, String, create_engine, Date, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
from Order import order
import time

conn = mysql.connector.connect(
    user='EasyCharge', password='XKThZNNwdTW7CMyy', database='easycharge')
cursor = conn.cursor(dictionary=True)


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
    'mysql+mysqlconnector://EasyCharge:XKThZNNwdTW7CMyy@localhost:3306/easycharge')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def getUsersNum():
    cursor.execute('SELECT MAX(id) FROM User')
    values = cursor.fetchone()
    # print(values)
    return values[0]


def insertUser(tmp_id, tmp_username, tmp_password, tmp_telephone, tmp_email):
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


def updateUser(tmp_id, tmp_username, tmp_password, tmp_telephone, tmp_email):
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


def getUserByName(tmp_username):
    session = DBSession()
    tmp = session.query(User).filter_by(username=tmp_username).first()
    if not tmp:
        return 0
    return tmp.id


def getAdminByName(tmp_Adminname):
    session = DBSession()
    tmp = session.query(Admin).filter_by(adminname=tmp_Adminname).first()
    if not tmp:
        return 0
    return tmp.id


def insertAdmin(tmp_id, tmp_Adminname, tmp_password, tmp_telephone, tmp_email):
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


def getAdminsNum():
    cursor.execute('SELECT MAX(id) FROM Admin')
    values = cursor.fetchone()
    # print(values)
    return values[0]


def getUserPassByName(tmp_username):
    session = DBSession()
    tmp = session.query(User).filter_by(username=tmp_username).first()
    if not tmp:
        return None
    return tmp.password


def getAdminPassByName(tmp_adminname):
    session = DBSession()
    tmp = session.query(Admin).filter_by(adminname=tmp_adminname).first()
    if not tmp:
        return None
    return tmp.password


def getUserPassById(tmp_id):
    session = DBSession()
    tmp = session.query(User).filter_by(id=tmp_id).first()
    if not tmp:
        return None
    return tmp.password


def getAdminPassById(adminid):
    session = DBSession()
    tmp = session.query(Admin).filter_by(id=adminid).first()
    if not tmp:
        return None
    return tmp.password


def getOrdersNum():
    cursor.execute('SELECT MAX(id) FROM OrderList')
    values = cursor.fetchone()
    # print(values)
    return values[0]


def insertOrder(tmp_id, tmp_userid, tmp_status,  tmp_creatTime, tmp_mode, tmp_capacity, tmp_totalCapacity):
    session = DBSession()
    orderlist = OrderList(
        id=tmp_id,
        user_id=tmp_userid,
        status=tmp_status,
        create_time=tmp_creatTime,
        mode=tmp_mode,
        capacity=tmp_capacity,
        totalCapacity=tmp_totalCapacity
    )
    session.add(orderlist)
    session.commit()
    tmp = session.query(OrderList).filter_by(id=tmp_id).first()
    if not tmp:
        return -1
    return 0


def updateOrder(tmp_id, tmp_userid, tmp_status,  tmp_creatTime, tmp_mode, tmp_capacity, tmp_totalCapacity):
    session = DBSession()
    tmp = session.query(OrderList).filter_by(id=tmp_id).first()
    if not tmp:
        return -2
    tmp.user_id = tmp_userid
    tmp.status = tmp_status
    tmp.create_time = tmp_creatTime
    tmp.mode = tmp_mode
    tmp.capacity = tmp_capacity
    tmp.totalCapacity = tmp_totalCapacity
    session.commit()
    test = session.query(OrderList).filter_by(id=tmp_id).first()
    if (test.user_id != tmp_userid or test.status != tmp_status or test.create_time != tmp_creatTime or
            test.mode != tmp_mode or test.capacity != tmp_capacity or test.totalCapacity != tmp_totalCapacity):
        return -1
    return 0

# 将订单状态改为4
# 表示已支付


def setOrderEnd(tmp_id):
    session = DBSession()
    tmp = session.query(OrderList).filter_by(id=tmp_id).first()
    if not tmp:
        return -2
    tmp.mode = 4
    session.commit()
    test = session.query(OrderList).filter_by(id=tmp_id).first()
    if test.mode != 4:
        return -1
    return 0


def getOrderDetailNum():
    cursor.execute('SELECT MAX(id) FROM ChargeInfo')
    values = cursor.fetchone()
    # print(values)
    return values[0]


def updateOrderDetail(tmp_id, tmp_creatTime, tmp_mode, tmp_capacity):
    session = DBSession()
    tmp = session.query(ChargeInfo).filter_by(id=tmp_id).first()
    if not tmp:
        return -2
    tmp.create_time = tmp_creatTime
    tmp.mode = tmp_mode
    tmp.charge_capacity = tmp_capacity
    test = session.query(ChargeInfo).filter_by(id=tmp_id).first()
    if (test.create_time != tmp_creatTime or test.mode != tmp_mode or test.charge_capacity != tmp_capacity):
        return -1
    return 0


def insertOrderDetail(tmp_id, tmp_orderid, tmp_creatTime, tmp_chargeId, tmp_curCap, tmp_totaltime,
                      tmp_startTime, tmp_endTime, tmp_capCost, tmp_serveCost, tmp_cost, tmp_mode):
    session = DBSession()
    chargeinfo = ChargeInfo(
        id=tmp_id,
        order_id=tmp_orderid,
        station_id=tmp_chargeId,
        start_time=tmp_startTime,
        stop_time=tmp_endTime,
        charge_capacity=tmp_curCap,
        cost=tmp_cost,
        create_time=tmp_creatTime,
        totaltime=tmp_totaltime,
        capCost=tmp_capCost,
        serveCost=tmp_serveCost,
        mode=tmp_mode
    )
    session.add(chargeinfo)
    session.commit()
    tmp = session.query(ChargeInfo).filter_by(id=tmp_id).first()
    if not tmp:
        return -1
    return 0

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
    session = DBSession()
    tmp = session.query(ChargeInfo).filter_by(ordier_id=tmp_orderid).first()
    if not tmp:
        return None
    orderdict = {
        'id': tmp.id,
        'orderid': tmp.order_id,
        'chargeId': tmp.station_id,
        'startTime': tmp.start_time,
        'endTime': tmp.stop_time,
        'chargeCapacity': tmp.charge_capacity,
        'cost': tmp.cost,
        'creatTime': tmp.create_time,
        'totaltime': tmp.totaltime,
        'capCost': tmp.capCost,
        'serveCost': tmp.serveCost,
        'mode': tmp.mode
    }
    return orderdict


# 传入一个用户id，返回该用户正在进行中的订单id
def getOrderingByUser(userid):
    session = DBSession()
    tmp = session.query(OrderList).filter(
        OrderList.user_id == userid, OrderList.mode != 4).first()
    if not tmp:
        return None
    return tmp.id


# 返回一个order类的对象
# 包含一下五个属性
# id, status, mode, capacity, createTime
# 失败返回None
def getOrderById(orderId):
    session = DBSession()
    tmp = session.query(OrderList).filter_by(id=orderId).first()
    if not tmp:
        return None
    result = order(tmp.id, tmp.status, tmp.mode, tmp.capacity, tmp.create_time)
    return result


# 返回用户userid的所有order 返回一个list list中每个元素是一个字典 存储order的信息
def getordersByUser(userid):
    session = DBSession()
    tmp = session.query(OrderList).filter_by(user_id=userid).all()
    if not tmp:
        return None
    listorder = []
    for row in tmp:
        orderdict = {
            'id': row.id,
            'userid': row.user_id,
            'status': row.status,
            'totalCapacity': row.totalCapacity,
            'capacity': row.capacity,
            'creatTime': row.create_time,
            'mode': row.mode
        }
        listorder.append(orderdict)
    return listorder


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
    startStruct = time.strptime(start, "%Y-%m-%d")
    startStamp = time.mktime(startStruct)
    endStruct = time.strptime(end, "%Y-%m-%d")
    endStamp = time.mktime(endStruct)
    session = DBSession()
    tmp = session.query(ChargeInfo).all()
    if (id != None):
        tmp = session.query(ChargeInfo).filter_by(station_id=id).all()
    if not tmp:
        return None
    listInfo = []
    for row in tmp:
        tmp_time = row.stop_time
        tmp_struct = time.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")
        tmp_stamp = time.mktime(tmp_struct)
        if (tmp_stamp >= startStamp and tmp_stamp <= endStamp):
            tmp_date = time.strptime("%Y-%m-%d", tmp_struct)
            orderdict = {
                "date": tmp_date,
                "pointID": row.station_id,
                "chargeTotalCnt": 33,
                "chargeTotalTime": 1457190363720,
                "chargeTotalElec": 70,
                "chargeTotalCcost": 50,
                "chargeTotalScost": 7,
                "chargeTotalcost": 12
            }
            listInfo.append(orderdict)
    return listInfo
