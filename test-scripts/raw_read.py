import serial
import time

ser = serial.Serial('/dev/ttyUSB1',9600)

message = bytearray();

def read():
	while ser.inWaiting() > 0 :
		enq = ser.read()
		foo = enq.encode('hex')
		message.append(foo.decode('hex'))
	output(message)
			

def parity(message):
	edb = 0
	for byte in message: edb ^= byte
	return edb;

def output(message):
	print "Outputing message:",
        for c in message:
		print bin(c)[2:].zfill(8),
	print

def process_message():
	global message
	tempmsg = message
	if parity(tempmsg) == 0:
		print "Got message 1"
		output(message)
		message = bytearray();
	elif len(tempmsg) > 2:
		print "Changing second byte"
		tempmsg[2] = 0x11;
		if parity(tempmsg) == 0:
			print "Got message 2"
			output(message)
			message = bytearray();



while 1 :
	if ser.inWaiting() > 0 :
		message = bytearray()
		read()
	time.sleep(1)


# Decode Elite Message
# Whenever the Elite makes a change to a loco state it sends a status broadcast.
#
# Consits of 5 bytes, which I think represent the following:
#
# Byte Number |    #1    |    #2     |    #3    |    #4     |    #5    |
# Meaning     |  Header  | Loco Addr | Unknown  | Speed/Dir |   XOR    |
# Example (1) | 00000000 | 00000011  | 00001100 | 10011011  | 10001001 |
# Example (2) | 00000000 | 00000011  | 00001100 | 10000111  | 10010101 |
# 
# So the data stream for example 1 can be read as:
#  #1 : Loco Status Broadcast
#  #2 : Loco Number 3
#  #3 : UNKNOWN
#  #4 : Bit0 ({1}0011011)- Direction of Loco, in this case it is set to 1, so it is going forward
#     : Bits1-7 (1{0011011}) - Speed of loco (in this case 51)
#  #5 : The XOR - In order to calculate the XOR, according to the standard you XOR the address byte (#2) with the data bytes (#3 and #4), however if you attempt this, then all the XOR bytes are wrong. To fix you have to interpret #3 as being 0001001 (0x11). at all times! WTF! 

