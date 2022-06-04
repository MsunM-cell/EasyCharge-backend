import Queue


class waitingArea(object):
    def __init__(self):
        self.fastQue = Queue.Queue(maxsize=2)
        self.tardyQue = Queue.Queue(maxsize=4)

    def haveEmpty(self, mode):
        if(mode == 0):
            # 快充
            if(not self.fastQue.full):
                return True
            else:
                return False
        else:
            # 慢充
            if(not self.tardyQue.full):
                return True
            else:
                return False

    def callin(self, order):
        if(order.mode == 0):
            # 快充
            if(not self.fastQue.full):
                self.fastQue.put(order)
                return True
            else:
                return False
        else:
            # 慢充
            if(not self.tardyQue.full):
                self.tardyQue.put(order)
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
            return -1
        else:
            for item in self.tardyQue.array:
                i += 1
                if(item.id == id):
                    return i
            return -1
    
    def setMode(self,id,mode):
        if(mode==0):#请求修改为快充，当前为慢充
            for item in self.tardyQue.array:
                if(item.id == id):
                    item.mode=0
                    return True
            return False
        else:
            for item in self.fastQue.array:
                if(item.id == id):
                    item.mode=1
                    return True
            return False

    def setCapacity(self,id,capacity):
        for item in self.fastQue.array:
            if(item.id == id):
                item.capacity=capacity
                return True
        for item in self.tardyQue.array:
            if(item.id == id):
                item.capacity=capacity
                return True
        return False
        



