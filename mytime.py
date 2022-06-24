
import time
#1655329800  2022-06-16 5:50:00     
timestamp=1655329800
startTime=int(time.time())

def mytime(): #time()
    return (int(time.time())-startTime)*10+timestamp

def mystrftime(str):
    return time.strftime(str,time.localtime(mytime()))

#print(strftime("%Y-%m-%d %H:%M:%S"))
def mylocaltime():
    return time.localtime(mytime())

