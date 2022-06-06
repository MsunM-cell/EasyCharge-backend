class Queue():
    def __init__(self, maxsize):
        self.array = list()
        self.maxsize = maxsize

    def length(self):
        if not self.array:
            return 0
        else:
            return len(self.array)

    def isEmpty(self):
        if(len(self.array)):
            return False
        else:
            return True

    def isFull(self):
        if(len(self.array) == self.maxsize):
            return True
        else:
            return False

    def push(self, value):
        self.array.append(value)

    def pop(self):
        return self.array.pop(0)

    def getItem(self, pos):
        if(pos<len(self.array)):
            return self.array[pos]
        else:
            return None
