import Queue
import Order
import threading
import time


class Charge():
    num = 1

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
        self.usable = True  # 是否故障
        self.useTimes = 0  # 累计充电次数
        self.chargeTime = 0  # 充电总时长
        self.chargeCap = 0  # 充电总电量

        # 需要充电的时间
        self.isOpen = True  # 充电桩开关
        self.priceThread = threading.Thread(target=self.setPrice)  # 价格调整线程
        self.priceThread.start()
        self.runThread = threading.Thread(target=self.Running)  # 充电桩主线程
        self.runThread.start()
    # 启动充电桩

    def Running(self):
        while(True):
            if(self.isOpen and not self.que.isEmpty() and not self.using):
                self.startCharge()
            time.sleep(5)
        # 循环判断是不是空，不是空且未开始充电则开始充电

    def haveEmpty(self):
        return not self.que.isFull()

    def getFirst(self):
        if(not self.que.isEmpty):
            return self.que.getItem(0)
        return None

    def getSecond(self):
        if(not self.que.isEmpty):
            return self.que.getItem(1)
        return None

    def getQueNum(self):
        return self.que.length()

    # 开始充电
    def startCharge(self):
        # using置为True
        # 计算充电时间
        self.using = True
        self.useTimes += 1
        self.getFirst().setStatus(2)
        self.time = 0
        self.cost = 0
        self.startTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.billing()

    def billing(self):
        while(self.using and self.usable):
            time.sleep(60)  # 测试时可以6秒模拟现实中的一分钟
            self.time += 60
            self.chargeTime += 60  # 总时长
            self.chargeCap = self.chargeTime/3600.0*self.power  # 总电量
            self.curCap = self.time/3600.0*self.power  # 充电量
            self.cost = self.cost+60/3600.0*self.power*self.price  # 充电费用
            if(self.curCap >= self.getFirst().capacity):
                break
        self.using = False
        self.endTime = time.strftime('%Y-%m-%d %H:%M:%S')
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

    def pushQue(self, order):
        self.que.push(order)

    def popQue(self):
        return self.que.pop()
# 0等候区/1排队中/2充电中/3待支付/4已支付/5已取消

    def endCharge(self):
        self.using = False

    def cancelOrder(self):
        self.que.getItem(1).setStatus(5)
        return self.que.array.pop(1)

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
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def dict(self):
        mydict = {
            "pointId": self.id,
            "status": int(not self.usable),
            "type": self.mode,
            "chargeCut": self.useTimes,
            "chargeTime": self.chargeTime,
            "chargeElec": self.chargeCap
        }
        return mydict