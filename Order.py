from os import stat
from tkinter import INSERT
import database
import time


class order(object):
    def __init__(self, id, status, mode, capacity, createTime):
        self.id = id
        self.status = status
        self.mode = mode
        self.capacity = capacity
        self.createTime = createTime

    def setStatus(self, status):
        self.status = status
        self.update()

    def update(self):
        database.updateOrder(self.id, self.createTime,
                             self.mode, self.capacity)

    def insert(self):
        database.insertOrder(self.id, self.createTime,
                             self.mode, self.capacity)


def createOrederDetail(orderid, chargeId, curCap, totaltime, startTime, endTime, capCost):
    id = database.getOrderDetailNum()+1
    creatTime = time.strftime('%Y-%m-%d %H:%M:%S')
    serveCost = 0.8*curCap
    cost = capCost+serveCost
    database.insertOrderDetail(id, orderid, creatTime, chargeId, curCap,
                               totaltime, startTime, endTime, capCost, serveCost, cost)
