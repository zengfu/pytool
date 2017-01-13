import serial
import re
import time

ip='52.74.236.46'
port='36003'
#ip='www.bananalife.top'
#port='7014'
cmd=[
    'AT^SISC=0'+'\r\n',
    'AT^SISS=0,srvType,STREAM\r\n',
    'AT^SISS=0,address,'+ip+'\r\n',
    'AT^SISS=0,port,'+port+'\r\n',
    'AT^SICI=0'+'\r\n',
    'AT^SISO=0'+'\r\n',
]
whd='AT^SISH=%d(0),0005000031\r\n'
rhd='AT^SISHR=0\r\n'
s=serial.Serial('COM20',115200,timeout=0.5)
s.write('\r\n')
for num,i in enumerate(cmd):
    s.write(i)
    data=s.read(100)
    s.flushInput()
    find=re.findall('OK',data)
    print data
    if not find:
        print 'fail'+str(num)
    else:
        print num
w=0
while True:
    w=w+1
    s.write(whd)
    time.sleep(0.1)
    length=s.inWaiting()
    data=s.read(length)
    data.replace('\r\n','')
    print 'send: '+data
    s.write(rhd)
    time.sleep(0.5)
    length=s.inWaiting()
    result=s.read(length)
    a=result.replace('\r\n', ',')
    length=len(a)
    print 'length: '+str(length)
    #re.findall('socket',result)
    print 'result:'+a
    time.sleep(2)
