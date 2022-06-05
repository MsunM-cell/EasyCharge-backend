from sqlalchemy import false, true
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
        thread.start()

    def haveEmpty(self):
        while(True):
            # 判断快充充电桩队列是否存在空位
            fast_have_empty = false
            for i in self.fastChargeList:
                if i.haveEmpty():
                    fast_have_empty = true
            if fast_have_empty:
                # 判断快充等候区有无订单
                fast_order = self.waitArea.callout(0)
                if fast_order != None:
                    # 找到匹配充电桩
                    fast_charge = self.fastSchedule()
                    fast_charge.pushQue(fast_order)
                    fast_order.setStatus(1)

            # 判断慢充充电桩队列是否存在空位
            slow_have_empty = false
            for i in self.slowChargeList:
                if i.haveEmpty():
                    slow_have_empty = true
            if slow_have_empty:
                # 判断慢充充等候区有无订单
                slow_order = self.waitArea.callout(1)
                if slow_order != None:
                    # 找到匹配充电桩
                    slow_charge = self.slowSchedule()
                    slow_charge.pushQue(slow_order)
                    slow_order.setStatus(1)

            time.sleep(5)

    def fastSchedule(self):
        # 首先判断有无故障充电桩
        # 只考虑单一充电桩故障且正好该充电桩有车排队的情况
        if self.badfastChargeList:
            # 故障采用优先级调度
            return self.badfastChargeList[0]

        # 没有故障充电桩的情况
        # 设置时间代价列表 (time, id)
        time_cost_list = list()
        # 遍历充电桩列表
        for i in self.fastChargeList:
            # 任意充电桩队列存在空位
            if (i.haveEmpty()):
                if (i.queue.isEmpty()):
                    time_cost_list.append((0, i.id))
                else:
                    time_cost = i.getFirst().capacity * 3600 / i.power - i.time
                    time_cost_list.append((time_cost, i.id))

        # 升序排列，返回时间代价最小的充电桩
        time_cost_list.sort()
        return time_cost_list[0]

    def slowSchedule(self):
        # 首先判断有无故障充电桩
        # 只考虑单一充电桩故障且正好该充电桩有车排队的情况
        if self.badtardyChargeList:
            # 故障采用优先级调度
            return self.badtardyChargeList[0]

        # 没有故障充电桩的情况
        # 设置时间代价列表 (time, id)
        time_cost_list = list()
        # 遍历充电桩列表
        for i in self.tardyChargeList:
            # 任意充电桩队列存在空位
            if (i.haveEmpty()):
                if (i.queue.isEmpty()):
                    time_cost_list.append((0, i.id))
                else:
                    time_cost = i.getFirst().capacity * 3600 / i.power - i.time
                    time_cost_list.append((time_cost, i.id))

        # 升序排列，返回时间代价最小的充电桩
        time_cost_list.sort()
        return time_cost_list[0]

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
