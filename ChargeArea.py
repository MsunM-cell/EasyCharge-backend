import charge
import threading
import time


class chargeArea(object):
    def __init__(self, waitArea):
        self.fastChargeList = list()
        self.tardyChargeList = list()
        self.badfastChargeList = list()
        self.badtardyChargeList = list()
        self.waitArea = waitArea
        # 2个快充
        self.fastChargeList.append(charge.Charge(0))
        self.fastChargeList.append(charge.Charge(0))
        # 3个慢充
        self.tardyChargeList.append(charge.Charge(1))
        self.tardyChargeList.append(charge.Charge(1))
        self.tardyChargeList.append(charge.Charge(1))
        thread = threading.Thread(target=self.haveEmpty)
        #thread.start()

    def haveEmpty(self):
        while(True):
            # 调度策略函数
            for i in self.fastChargeList:
                if(i.haveEmpty()):
                    # 如果有充电桩坏了 调入坏了的充电桩的队列  
                    # 充电桩的usable属性为False 即为坏了
                    # 调入时修改order订单状态 order.setStatus()
                    # if(self.badfastChargeList.)
                    order=self.waitArea.callout(0)
                    if(order!=None):
                        i.pushQue(order)

# list中的项目是充电桩
# time是已充电时长
# requestTime 是请求的总时长

            for i in self.tardyChargeList:
                if(i.haveEmpty()):
                    order=self.waitArea.callout(1)
                    if(order!=None):
                        i.pushQue(order)
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

    def getChargeById(self, id):
        for i in self.fastChargeList:
            if(i.id == id):
                return i
        for i in self.tardyChargeList:
            if(i.id == id):
                return i
        return None

    def openCharge(self, id):
        charge = self.getChargeById(id)
        if(charge != None):
            charge.open()
            return True
        else:
            return False

    def closeCharge(self, id):
        charge = self.getChargeById(id)
        if(charge != None):
            charge.close()
            return True
        else:
            return False

    def getChargeInfo(self):
        charge = self.getChargeById(id)
        if(charge != None):
            return charge.dict()
        else:
            return None

    def getChargingInfo(self, id):
        for i in self.fastChargeList:
            if(i.getFirst().id == id):
                return {
                    "station": i.id,
                    "capacity_cost": i.cost,
                    "service_cost": i.curCap*0.8,
                    "cost": i.cost+i.curCap*0.8,
                    "start_time": i.startTime,
                    "time": i.time,
                    "capacity": i.curCap
                }
            elif(i.getSecond().id == id):
                return{
                    "station": i.id
                }
        for i in self.tardyChargeList:
            if(i.getFirst().id == id):
                return {
                    "station": i.id,
                    "capacity_cost": i.cost,
                    "service_cost": i.curCap*0.8,
                    "cost": i.cost+i.curCap*0.8,
                    "start_time": i.startTime,
                    "time": i.time,
                    "capacity": i.curCap
                }
            elif(i.getSecond().id == id):
                return{
                    "station": i.id
                }
        return None

    def cancel(self, id):
        for i in self.fastChargeList:
            order = i.getFirst()
            if(order.id == id):
                i.endCharge()
                return order.json()
            elif(i.getSecond().id == id):
                return i.cancelOrder().json()
        for i in self.tardyChargeList:
            order = i.getFirst()
            if(order.id == id):
                i.endCharge()
                return order.json()
            elif(i.getSecond().id == id):
                return i.cancelOrder().json()
        return None

    def getAllPoints(self):
        List = list()
        for i in self.fastChargeList:
            List.append(i.dict())
        for i in self.tardyChargeList:
            List.append(i.dict())
        for i in self.badfastChargeList:
            List.append(i.dict())
        for i in self.badtardyChargeList:
            List.append(i.dict())
        return List

    def getWaitInfo(self, pointid):
        point = self.getChargeById(id)
        order = point.getSecond()
        if(order != None):
            return {
                "id": order.userid,
                "carElecTotal": order.totalCapacity,
                "carElecRequest": order.capacity,
                "carWaitTime": int(time.time-time.mktime(time.strptime(order.createTime, '%Y-%m-%d %H:%M:%S')))
            }
