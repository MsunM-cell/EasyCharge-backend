from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)



def getUsersNum():
    id = 1
    return id


def insertUser(id, username, passward, telephone, email):
    id = 1


def updateUser(id, username, passward, telephone, email):
    id = 1


def getUserByName(username):
    id = 1
    return 0


def getAdminByName(Adminname):
    id = 1


def insertAdmin(id, Adminnum, passward, telephone, email):
    id = 1


def getAdminsNum():
    id = 1


def getUserPassByName(username):
    id = 1


def getAdminPassByName(adminname):
    id = 1


def getUserPassById(id):
    id = 1


def getAdminPassById(adminid):
    id = 1


def getOrdersNum():
    id = 1


def insertOrder(id, userid, status, creatTime, mode, capacity,totalCapacity):
    id = 1


def updateOrder(id, userid, status, creatTime, mode, capacity,totalCapacity):
    id = 1


def setOrderEnd(id):
    id = 1
# 将订单状态改为4
# 表示已支付


def getOrderDetailNum():
    id = 1


def updateOrderDetail(id, creatTime, mode, capacity):
    id = 1


def insertOrderDetail(id, orderid, creatTime, chargeId, curCap,
                      totaltime, startTime, endTime, capCost, serveCost, cost):
    id = 1


def getOrderDetailByOrder(orderid):
    # 将详单各字段通过字典返回
    id = 1
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


def getOrderingByUser(id):
    id = 1
    # 传入一个用户id，返回该用户正在进行中的订单id


def getOrderById(orderId):
    id = 1
    # 返回一个order类的对象
    # 包含一下五个属性
    # id, status, mode, capacity, createTime
    # 失败返回None

def getordersByUser(userid):
    id=1
    # 返回用户userid的所有order 返回一个list list中每个元素是一个字典 存储order的信息

def getPointReport(start,end,id):
    #id为空 表示所有充电桩 否则只选该id充电桩
    #返回选中充电桩时间范围内每一天的的总充电量
    #日期、充电桩编号、累计充电次数、累计充电时长、累计充电量、累计充电费用、累计服务费用、累计总费用
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
    #     },
    #     {

    #     }

    # ]
    id=1



