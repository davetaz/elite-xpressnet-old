import sys
import serial
import time

ser = serial.Serial('/dev/ttyUSB1',9600)

def send(message):
	ok = False
	trys = 1
	while (not ok and trys < 5) :
	  ser.write(message)
	  print 'trys = %d send:' % (trys) , 
	  for byte in message:print(hex(byte)) ,
	  time.sleep(.1)
	  print ' receive: ',     
	  while ser.inWaiting() > 0 :
	  	enq = ser.read()
	  	print enq.encode('hex') ,  
	  	if enq == '05'.decode('hex') : 
		  ok = True
	  print 
	  trys += 1

def parity(message):
	edb = 0
	for byte in message: edb ^= byte
	message.append(edb)

def setThrottle(address,direction,speed):
	message = bytearray('E400000000'.decode('hex'))
	message[1] = 0x13
	message[3] = address
	message[4] = speed
	if direction  == 'f' : message[4] |= int(b'10000000',2)
	elif direction =='b' : message[4] &= int(b'01111111',2)
	parity(message) 
	send(message) 
#	test(message)

def getFirmwareVersion():
	message = bytearray('212100'.decode('hex'))
	send(message)

def test(message):
	for c in message: print(c)


print "Loco: " + sys.argv[1]
print "Direction: " + sys.argv[2]
print "Speed: " + sys.argv[3]
#setThrottle(3,"b",0);
setThrottle(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]));
#getFirmwareVersion()
