from os import stat
import database
import time
class order(object):
    def __init__(self,status,mode,capacity):
        self.status=status
        self.mode=mode
        self.capacity=capacity
        self.creatTime=time.strftime('%Y-%m-%d %H:%M:%S')
    
    def setId(self,id):
        self.id=id

    def setStatus(self,status):
        self.status=status

    def update(self):
        database.updateOrder(self.id,self.creatTime,self.mode,self.capacity)
    
    def insert(self):
        database.insertOrder(self.id,self.creatTime,self.mode,self.capacity)