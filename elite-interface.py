import serial
import time
import redis

ser = serial.Serial('/dev/ttyUSB1',9600)

message = bytearray()
r = redis.Redis()

def read():
	while ser.inWaiting() > 0 :
		enq = ser.read()
		foo = enq.encode('hex')
		message.append(foo.decode('hex'))
		if len(message) > 2:
			process_message()
			

def parity(tempmsg,header):
	if header:
		tempmsg[0] = header
	edb = 0
	for byte in tempmsg: edb ^= byte
	return edb;

def output(message):
	print "Outputing message:",
        for c in message:
		print bin(c)[2:].zfill(8),
	print

def process_message():
	global message
	global r
	tempmsg = message
	done = 0
	message_type = "unknown";

	if parity(tempmsg,0x1d) == 0:
#		print "Speed/Direction Change"
		message_type = "s/d";
		loco = message[1];
		direction = get_direction(message[3]);
		speed = message[3];
		if (speed > 127):
			speed = speed - 128
		r.rpush('loco','s/d,' + str(loco) + ',' + direction + ',' + str(speed)); 
		done = 1
	elif parity(tempmsg,0x1c) == 0:
#		print "Function Change"
		loco = message[1];
		message_type = "f";
		functions = get_functions_1(message[2]);
		functions = get_functions_2(message[3],functions);
		functions = bin(functions)[2:].zfill(16)
		r.rpush('loco','f,' + str(loco) + ',' + functions); 
		done = 1
	elif parity(tempmsg,None) == 0:
#		print "Raw Message"
		done = 1
	
	if done > 0 :
#		output(message)
		message = bytearray();


def get_direction(byte):
	if (byte & 128):
		return "r";
	return "f";

def get_functions_1(byte):
	functions = 0
	if (byte & 16):
		functions = functions | 1
	if (byte & 1):
		functions = functions | 2
	if (byte & 2):
		functions = functions | 4
	if (byte & 4):
		functions = functions | 8
	if (byte & 8):
		functions = functions | 16
	return functions;

def get_functions_2(byte,functions):
	if (byte & 1):
		functions = functions | 32
	if (byte & 2):
		functions = functions | 64
	if (byte & 4):
		functions = functions | 128
	if (byte & 8):
		functions = functions | 256
	if (byte & 16):
		functions = functions | 512
	if (byte & 32):
		functions = functions | 1024
	if (byte & 64):
		functions = functions | 2048
	if (byte & 128):
		functions = functions | 4096
	return functions;

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
#  #5 : The XOR - In order to calculate the XOR, according to the standard you XOR the address byte (#2) with the data bytes (#3 and #4), however if you attempt this, then all the XOR bytes are wrong. To fix you have to guess what the propper value of #1 should be and then XOR this byte with the rest as well. Problem is the header byte changes dependant on the function being performed. Here is my break down so far:
#
# HEADER BYTES with the elite
# It likes sending 00000000, this is wrong I think, here is what I have discovered:
#   #1 : 00011101 (0x1d) will XOR to give a speed or direction change
#   #1 : 00011100 (0x1c) will XOR to give a function change, e.g. tunring a function on or off. More soon...

