from ast import Num
from multiprocessing.connection import wait
import Queue
import Order
import threading
import time

class Charge():
    num = 0
    def __init__(self, mode):
        self.mode = mode
        self.using = False
        self.id = Charge.num
        Charge.num += 1
        self.que = Queue.Queue(2)
        if(mode == 0):
            self.power = 30
        else:
            self.power = 7
        self.usable = True  #是否故障
        self.useTimes=0 #累计充电次数
        self.chargeTime=0   #充电总时长
        self.chargeCap=0    #充电总电量
        self.open=True  #充电桩开关
        self.priceThread = threading.Thread(target=self.setPrice)  # 价格调整线程
        self.priceThread.start()
        self.runThread = threading.Thread(target=self.Running)  # 充电桩主线程
        self.runThread.start()
    # 启动充电桩

    def Running(self):
        while(True):
            if(self.open and not self.que.isEmpty() and not self.using):
                self.startCharge()
            time.sleep(5)
        # 循环判断是不是空，不是空且未开始充电则开始充电

    def haveEmpty(self):
        return not self.que.isFull()

    def getFirst(self):
        if(not self.que.isEmpty):
            return self.que.getItem(0)

    def getQueNum(self):
        return self.que.length()

    # 开始充电
    def startCharge(self):
        # using置为True
        # 计算充电时间
        self.using = True
        self.getFirst().setStatus(2)
        self.time = 0
        self.cost = 0
        self.startTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.billing()

    def billing(self):
        while(self.using and self.usable):
            time.sleep(60)  # 测试时可以6秒模拟现实中的一分钟
            self.time += 60
            self.curCap = self.time/3600.0*self.power  # 充电量
            self.cost = self.cost+60/3600.0*self.power*self.price  # 充电费用
            if(self.curCap >= self.getFirst().capacity):
                break
        self.endCharge()

    def pushQue(self, order):
        self.que.push(order)

    def popQue(self):
        return self.que.pop()
# 0等候区/1排队中/2充电中/3待支付/4已支付/5已取消

    def endCharge(self):
        self.endTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.using = False
        completeOrder = self.popQue()
        completeOrder.setStatus(3)
        # 产生详单
        # 详单编号 从数据库获得
        # 详单生成时间(无需存储，请求时计算)
        # 充电桩编号id、充电电量curCap、充电时长time、
        # 启动时间startTime、停止时间endTime、充电费用cost、服务费用0.8*curCap、
        # 总费用 ；
        Order.createOrederDetail(completeOrder.id, self.id, self.curCap,
                                 self.time, self.startTime, self.endTime, self.cost)

    def setPrice(self):
        while(True):
            curHour = time.localtime().tm_hour
            if((curHour >= 10 and curHour < 15) or (curHour >= 18 and curHour < 21)):
                self.price = 1.0
            elif(curHour >= 23 or curHour < 7):
                self.price = 0.4
            else:
                self.price = 0.7
            time.sleep(60)

    def setError(self):
        self.usable = False
    
    def open(self):
        self.open=True
    def close(self):
        self.open=False

    def dict(self):
        mydict={
            "pointId":self.id,
            "status":int(not self.usable),
            "type":self.mode,
            "chargeCut":self.useTimes,
            "chargeTime":self.chargeTime,
            "chargeElec":self.chargeCap
        }
        return mydict



class chargeArea(object):
    def __init__(self, waitArea):
        self.fastChargeList = list()
        self.tardyChargeList = list()
        self.badChargeList = list()
        self.waitArea = waitArea
        # 2个快充
        self.fastChargeList.append(Charge(0))
        self.fastChargeList.append(Charge(0))
        # 3个慢充
        self.tardyChargeList.append(Charge(1))
        self.tardyChargeList.append(Charge(1))
        self.tardyChargeList.append(Charge(1))
        thread = threading.Thread(target=self.haveEmpty)

    def haveEmpty(self):
        while(True):
            # 调度策略函数
            for i in self.fastChargeList:
                if(i.haveEmpty()):
                    # 如果有充电桩坏了 调入坏了的充电桩的队列
                    # 调入时修改order订单状态
                    i.pushQue(self.waitArea.callout(0))
            for i in self.tardyChargeList:
                if(i.haveEmpty()):
                    i.pushQue(self.waitArea.callout(1))
            time.sleep(5)


    def getModeNum(self, mode):
        # 获取特定模式下的车辆数量
        result = 0
        if(mode == 0):
            for i in self.fastChargeList:
                result += i.getQueNum()
        else:
            for i in self.tardyChargeList:
                result += i.getQueNum()
        return result

    def getChargeById(self,id):
        for i in self.fastChargeList:
            if(i.id==id):
                return i
        for i in self.tardyChargeList:
            if(i.id==id):
                return i
        return None
    
    def openCharge(self,id):
        charge=self.getChargeById(id)
        if(charge!=None):
            charge.open()
            return True
        else:
            return False
    
    def closeCharge(self,id):
        charge=self.getChargeById(id)
        if(charge!=None):
            charge.close()
            return True
        else:
            return False

    def getChargeInfo(self):
        charge=self.getChargeById(id)
        if(charge!=None):
            return charge.dict()
        else:
            return None

