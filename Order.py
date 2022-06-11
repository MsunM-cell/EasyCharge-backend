import database
import time


class order(object):
    def __init__(self, id, userid, status, mode, capacity, createTime,totalCapacity=999999):
        self.id = id
        self.userid = userid
        self.status = status
        self.mode = mode
        self.capacity = capacity
        self.createTime = createTime
        self.totalCapacity=totalCapacity

    def setStatus(self, status):
        self.status = status
        self.update()

    def update(self):
        if(self.totalCapacity==None):
            self.totalCapacity=0
        database.updateOrder(self.id, self.userid, self.status, self.createTime,
                             self.mode, self.capacity,self.totalCapacity)

    def insert(self):
        if(self.totalCapacity==None):
            self.totalCapacity=0
        database.insertOrder(self.id, self.userid, self.status, self.createTime,
                             self.mode, self.capacity,self.totalCapacity)

    def json(self):
        return {
            "id": self.id,
            "status": self.status,
            "createTime": self.createTime,
            "mode": self.mode,
            "capacity": self.capacity
        }


def createOrederDetail(orderid, chargeId, curCap, totaltime, startTime, endTime, capCost,mode):
    id = database.getOrderDetailNum()+1
    creatTime = time.strftime('%Y-%m-%d %H:%M:%S')
    serveCost = 0.8*curCap
    cost = capCost+serveCost
    database.insertOrderDetail(id, orderid, creatTime, chargeId, curCap,
                               totaltime, startTime, endTime, capCost, serveCost, cost,mode)
