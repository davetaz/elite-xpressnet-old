import smbus
import redis

redis = redis.Redis()

bus = smbus.SMBus(1)
#addresses = [0x20,0x21]
addresses = [0x20]

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

prev = {}

for address in addresses:
	bus.write_byte_data(address,IODIRA,0xff)
	bus.write_byte_data(address,IODIRB,0x00)

	bus.write_byte_data(address,GPPUA,0xff)
	bus.write_byte_data(address,GPINTENA,0xff)

	status = bus.read_byte_data(address,0x13)
	bus.write_byte_data(address,0x13,int(status))
	prev[address]=255

while 1 :
	for address in addresses:
		state = bus.read_byte_data(address,INTCAPA)
		mask = 255
		back = mask - state
		if (back > 0 and back != prev[address]):
			prev[address] = back
			active = str(address) + ",A," + str(back)
			print "sensors " + active
			redis.rpush("sensors",active)
		if (state == 255):
			prev[address] = 255
