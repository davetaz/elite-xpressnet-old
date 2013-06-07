import smbus
import time

bus = smbus.SMBus(1)
address = 0x20

IODIRA =  0x00 
IODIRB =  0x01
GPINTENA = 0X04
GPINTENB = 0x05
GPPUA  =  0x0c
GPPUB  =  0x0d
INTFA  =  0x0e
INTFB  =  0x0f
INTCAPA=  0x10
INTCAPB=  0x11
GPIOA  =  0x12
GPIOB  =  0x13

bus.write_byte_data(address,IODIRA,0xff)
bus.write_byte_data(address,IODIRB,0x00)

bus.write_byte_data(address,GPPUA,0xff)
bus.write_byte_data(address,GPINTENA,0xff)

status = bus.read_byte_data(address,0x13)
print status
bus.write_byte_data(address,0x13,0)

while 1 :
	x=bus.read_byte_data(address,INTFA)
	if (x & 0x01) : 
		print 'Sensor 1'
		x=bus.read_byte_data(address,INTCAPA)
		print bin(x)[2:].zfill(8)
