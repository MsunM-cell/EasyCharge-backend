import Queue


class waitingArea(object):
    totalNum=10
    curNum=0
    def __init__(self):
        self.fastQue = Queue.Queue(maxsize=waitingArea.totalNum)
        self.tardyQue = Queue.Queue(maxsize=waitingArea.totalNum)

    def haveEmpty(self):
        if(waitingArea.curNum<waitingArea.totalNum):
            return True
        else:
            return False

    def callin(self, order):

        if(order.mode == 0):
            # 快充

            if(not self.fastQue.isFull() and self.haveEmpty()):
                self.fastQue.push(order)
                return True
            else:
                return False
        else:
            # 慢充
            if(not self.tardyQue.isFull() and self.haveEmpty()):
                self.tardyQue.push(order)
                return True
            else:
                return False

    def callout(self, mode):
        if(mode == 0):
            # 快充
            if(self.fastQue.isEmpty()):
                return None
            else:
                return self.fastQue.pop()
        else:
            # 慢充
            if(self.tardyQue.isEmpty()):
                return None
            else:
                return self.tardyQue.pop()

    def getQuepos(self, id, mode):
        # 取等候区中车辆的位置
        i = 0
        if(mode == 0):
            for item in self.fastQue.array:
                i += 1

                if(item.id == id):
                    
                    return i
            return 1
        else:
            for item in self.tardyQue.array:
                i += 1
                if(item.id == id):
                    return i
            return 1
    
    def setMode(self,id,mode):
        
        if(mode==0):#请求修改为快充，当前为慢充
            for item in self.tardyQue.array:
                if(item.id == id):
                    item.mode=0
                    item.update()
                    temp=self.tardyQue.pop()
                    self.fastQue.push(temp)
                    return True
            return False
        else:
            for item in self.fastQue.array:
                if(item.id == id):
                    item.mode=1
                    item.update()
                    temp=self.fastQue.pop()
                    self.tardyQue.push(temp)
                    return True
            return False

    def setCapacity(self,id,capacity):
        for item in self.fastQue.array:
            if(item.id == id):
                item.capacity=capacity
                item.update()
                return True
        for item in self.tardyQue.array:
            if(item.id == id):
                item.capacity=capacity
                item.update()
                return True
        return False
        
    def getAllWaitInfo(self):
        list=[]
        for i in self.fastQue.array:
            car={
                "orderid":i.id,
                "mode":i.mode,
                "capacity":i.capacity
            }
            list.append(car)
        for i in self.tardyQue.array:
            car={
                "orderid":i.id,
                "mode":i.mode,
                "capacity":i.capacity
            }
            list.append(car)
        return list


