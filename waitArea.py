import Queue


class waitingArea(object):
    fastWaitNum=2 #快充等待数量
    tardyWaitNum=4 #慢充等待数量
    def __init__(self):
        self.fastQue = Queue.Queue(maxsize=waitingArea.fastWaitNum)
        self.tardyQue = Queue.Queue(maxsize=waitingArea.tardyWaitNum)

    def haveEmpty(self, mode):
        if(mode == 0):
            # 快充
            if(not self.fastQue.isFull()):
                return True
            else:
                return False
        else:
            # 慢充
            if(not self.tardyQue.isFull()):
                return True
            else:
                return False

    def callin(self, order):

        if(order.mode == 0):
            # 快充

            if(not self.fastQue.isFull()):
                self.fastQue.push(order)
                return True
            else:
                return False
        else:
            # 慢充
            if(not self.tardyQue.isFull()):
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
        



