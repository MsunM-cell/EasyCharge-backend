
import time
#1655329800  2022-06-16 5:50:00     
timestamp=1655329800
localtime=int(time.time())
timestamp=localtime-timestamp

def mytime(): #time()
    return int(time.time())-timestamp

def mystrftime(str):
    return time.strftime(str,time.localtime(mytime()))

#print(strftime("%Y-%m-%d %H:%M:%S"))
def mylocaltime():
    return time.localtime(mytime())





