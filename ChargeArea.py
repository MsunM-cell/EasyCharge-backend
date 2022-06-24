from sqlalchemy import false, true
import charge
import threading
import time
import mytime


class chargeArea(object):
    fastNum=2 #快充数量
    tardyNum=3 #慢充数量
    def __init__(self, waitArea):
        self.fastChargeList = list()
        self.tardyChargeList = list()
        self.badfastChargeList = list()
        self.badtardyChargeList = list()
        self.waitArea = waitArea
        self.waitStop=False
        # 2个快充
        for i in range(chargeArea.fastNum):
            self.fastChargeList.append(charge.Charge(0))
        
        # 3个慢充
        for i in range(chargeArea.tardyNum):
            self.tardyChargeList.append(charge.Charge(1))
        
        thread = threading.Thread(target=self.haveEmpty)
        thread.start()

   
    def haveEmpty(self):
        while(True):
            # 判断快充充电桩队列是否存在空位
            # fast_have_empty = false
            if(not self.waitStop):
                for i in self.fastChargeList:
                    if i.haveEmpty():
                #         fast_have_empty = true
                # if fast_have_empty:
                    # 判断快充等候区有无订单
                        fast_order=None
                        if self.badfastChargeList:
                            # 故障采用优先级调度
                            time.sleep(5)
                            if(self.badfastChargeList):
                                fast_order=self.badfastChargeList[0].popQue()
                                if(fast_order==None):
                                    fast_order = self.waitArea.callout(0)
                        else:
                            fast_order = self.waitArea.callout(0)
                        if fast_order != None:
                            # 找到匹配充电桩
                            fast_charge = self.fastSchedule()
                            fast_charge.pushQue(fast_order)
                            fast_order.setStatus(1)            

                # 判断慢充充电桩队列是否存在空位
                # slow_have_empty = false
                for i in self.tardyChargeList:
                    if i.haveEmpty():
                #         slow_have_empty = true
                # if slow_have_empty:
                    # 判断慢充充等候区有无订单
                        slow_order=None
                        if self.badtardyChargeList:
                            time.sleep(5)
                            # 故障采用优先级调度
                            if(self.badtardyChargeList):
                                slow_order=self.badtardyChargeList[0].popQue()
                                if(slow_order==None):
                                    slow_order = self.waitArea.callout(1)
                        else:
                            slow_order = self.waitArea.callout(1)
                        
                        if slow_order != None:
                            # 找到匹配充电桩
                            
                            slow_charge = self.slowSchedule()

                            slow_charge.pushQue(slow_order)
                            slow_order.setStatus(1)
            else:
                time.sleep(1)
    def recoverySchedule(self):
        self.waitStop=True
        list=[]
        for charge in self.fastChargeList:
            waitList=charge.popWait()
            if(waitList!=None and len(waitList)!=0):
                for order in waitList:
                    list.append(order)
        for charge in self.tardyChargeList:
            waitList=charge.popWait()
            if(waitList!=None and len(waitList)!=0):
                for order in waitList:
                    list.append(order)
        while list:
            for charge in self.fastChargeList:
                if(charge.haveEmpty()):
                    for index in range(len(list)):
                        if(list[index]!=None and list[index].mode==0):
                            order=list.pop(index)
                            fast_charge = self.fastSchedule()
                            fast_charge.pushQue(order)
                            order.setStatus(1)
                            break;  
                        else:
                            continue
            for charge in self.tardyChargeList:
                if(charge.haveEmpty()):
                    for index in range(len(list)):
                        if(list[index]!=None and list[index].mode==1):
                            order=list.pop(index)
                            fast_charge = self.slowSchedule()
                            fast_charge.pushQue(order)
                            order.setStatus(1)
                            break;  
                        else:
                            continue
        self.waitStop=False     
                              
    def fastSchedule(self):
        
        # 设置时间代价列表 (time, id)
        time_cost_list = list()
        # 遍历充电桩列表
        for i in self.fastChargeList:
            # 任意充电桩队列存在空位
            if (i.haveEmpty()):
                if (i.que.isEmpty()):
                    time_cost_list.append((0, i.id))
                else:
                    time_cost=0
                    for temp in i.que.array:
                        time_cost += temp.capacity * 3600 / i.power - i.time
                    time_cost_list.append((time_cost, i.id))

        # 升序排列，返回时间代价最小的充电桩
        time_cost_list.sort()
        return self.getChargeById(time_cost_list[0][1]) 

    def slowSchedule(self):
        # 没有故障充电桩的情况
        # 设置时间代价列表 (time, id)
        time_cost_list = list()
        # 遍历充电桩列表
        for i in self.tardyChargeList:
            # 任意充电桩队列存在空位
            if (i.haveEmpty()):
                if (i.que.isEmpty()):
                    time_cost_list.append((0, i.id))
                else:
                    time_cost=0
                    for temp in i.que.array:
                        time_cost += temp.capacity * 3600 / i.power - i.time
                    time_cost_list.append((time_cost, i.id))

        # 升序排列，返回时间代价最小的充电桩
        time_cost_list.sort()
        return self.getChargeById(time_cost_list[0][1]) 

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

    def setChargeError(self,id):
        for index,i in enumerate(self.fastChargeList):
            if(i.id == id):
                i.setUsable(False)
                charge=self.fastChargeList.pop(index)
                self.badfastChargeList.append(charge)

                return True
        for index,i in enumerate(self.tardyChargeList):
            if(i.id == id):
                i.setUsable(False)
                charge=self.tardyChargeList.pop(index)
                self.badtardyChargeList.append(charge)
                return True
        return False

    def setChargeOK(self,id):
        for index,i in enumerate(self.badfastChargeList):
            if(i.id == id):
                i.setUsable(True)
                charge=self.badfastChargeList.pop(index)
                self.fastChargeList.append(charge)
                self.recoverySchedule()
                return True
        for index,i in enumerate(self.badtardyChargeList):
            if(i.id == id):
                i.setUsable(True)
                charge=self.badtardyChargeList.pop(index)
                self.tardyChargeList.append(charge)
                self.recoverySchedule()
                return True
        return False
        
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
            
            if(i.getFirst()!=None and i.getFirst().id == id):
                return {
                    "station": i.id,
                    "capacity_cost": round(i.cost,2),
                    "service_cost": round(i.curCap*0.8,2),
                    "cost": round(round(i.cost,2)+round(i.curCap*0.8,2),2),
                    "start_time": i.startTime,
                    "time": i.time,
                    "capacity": round(i.curCap,2)
                }
            else:
                for temp in i.getWait():
                    if(temp!=None and temp.id==id):
                        return{
                            "station": i.id
                        }
        for i in self.tardyChargeList:
            if(i.getFirst()!=None and i.getFirst().id == id):
                return {
                    "station": i.id,
                    "capacity_cost": round(i.cost,2),
                    "service_cost": round(i.curCap*0.8,2),
                    "cost": round(round(i.cost,2)+round(i.curCap*0.8,2),2),
                    "start_time": i.startTime,
                    "time": i.time,
                    "capacity": round(i.curCap,2)
                }
            else:
                for temp in i.getWait():
                    if(temp!=None and temp.id==id):
                        return{
                            "station": i.id
                        }
        return None

    def cancel(self, id):
        for i in self.fastChargeList:
            order = i.getFirst()
            if( order!= None and order.id == id):
                i.endCharge()
                return order.json()
            else:
                for index,temp in enumerate(i.getWait()):
                    if(temp!=None and temp.id==id):
                        return i.cancelOrder(index).json()
        for i in self.tardyChargeList:
            order = i.getFirst()
            if(order != None and order.id == id):
                i.endCharge()
                return order.json()
            else:
                for index,temp in enumerate(i.getWait()):
                    if(temp!=None and temp.id==id):
                        return i.cancelOrder(index).json()
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

    def getAllInfo(self):
        resultDict = {}
        for i in self.fastChargeList:
            resultDict[i.id]=i.getInfo()
        for i in self.tardyChargeList:
            resultDict[i.id]=i.getInfo()
        for i in self.badfastChargeList:
            resultDict[i.id]=i.getInfo()
        for i in self.badtardyChargeList:
            resultDict[i.id]=i.getInfo()
        return resultDict

    def getBadChargeById(self, id):
        for i in self.badfastChargeList:
            if(i.id == id):
                return i
        for i in self.badtardyChargeList:
            if(i.id == id):
                return i
        return None

    def getWaitInfo(self, pointid):
        point = self.getChargeById(pointid)
        if(point == None):
            point = self.getBadChargeById(pointid)
            if(point == None):
                return None
        order = point.getWait()
        if(order != None):
            list=[]
            for temp in order:
                dict={
                "id": temp.userid,
                "carElecTotal": temp.totalCapacity,
                "carElecRequest": temp.capacity,
                "carWaitTime": int(mytime.mytime()- time.mktime(time.strptime(temp.createTime, '%Y-%m-%d %H:%M:%S')))
                }
                list.append(dict)
            return list
        else:
            return []
        
