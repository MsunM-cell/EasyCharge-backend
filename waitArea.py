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
            if(self.fastQue.empty()):
                return None
            else:
                return self.fastQue.pop()
        else:
            # 慢充
            if(self.tardyQue.empty()):
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
