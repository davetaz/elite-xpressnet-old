# Overview
# This script should take a signals id (e.g. 32,B,16) and the color this signal needs to be.
# In order to manage the signals we will need to load a new signals object for each signal based upon the ids. 
# In order to change the signal we need to work out the mask for the pins dictated by the number of aspects. 
# Later the number of aspects will also include feathers so you could have a signal that uses all 8 control channels on a single mcp23017 chip (A or B).
# To change the mask we need to get the state of the current channel, shift the bits to match our new signal and write this back out. 
# Example 
# change_signal("32,B,16",green)
# 
import smbus
import time
import sys
import redis

redis = redis.Redis()

bus = smbus.SMBus(1)
address = 0x00
if (int(sys.argv[1]) == 1 or int(sys.argv[1]) == 2): 
	address = 0x20
if (int(sys.argv[1]) == 3 or int(sys.argv[1]) == 4): 
	address = 0x21

if (address == 0x00):
	print "No Controller Selected!"
	sys.exit()

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

state = bus.read_byte_data(address,0x13);
#print state

signal1 = 0
signal2 = 0
if (state & 0x01):
	signal1 = 1
if (state & 0x02):
	signal1 = 2
if (state & 0x04):
	signal1 = 4
if (state & 0x08):
	signal1 = 8

if (state & 0x10):
	signal2 = 16
if (state & 0x20):
	signal2 = 32
if (state & 0x40):
	signal2 = 64
if (state & 0x80):
	signal2 = 128

#print "Signal 1: " + str(signal1)
#print "Signal 2: " + str(signal2)

def isodd(num):
        return num & 1

if (len(sys.argv) < 3):
	bus.write_byte_data(address,0x13,0)
	bus.write_byte_data(address,0x13,int(sys.argv[1]))
	exit	

if (isodd(int(sys.argv[1])) and str(sys.argv[2]) == "amber2"):
	bus.write_byte_data(address,0x13,signal2)
	newstate = 1 + signal2
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) and str(sys.argv[2]) == "red"):
	bus.write_byte_data(address,0x13,signal2)
	newstate = 2 + signal2
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) and str(sys.argv[2]) == "amber"):
	bus.write_byte_data(address,0x13,signal2)
	newstate = 4 + signal2
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) and str(sys.argv[2]) == "green"):
	bus.write_byte_data(address,0x13,signal2)
	newstate = 8 + signal2
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) == 0 and str(sys.argv[2]) == "green"):
	bus.write_byte_data(address,0x13,signal1)
	newstate = 16 + signal1
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) == 0 and str(sys.argv[2]) == "amber"):
	bus.write_byte_data(address,0x13,signal1)
	newstate = 32 + signal1
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) == 0 and str(sys.argv[2]) == "red"):
	bus.write_byte_data(address,0x13,signal1)
	newstate = 64 + signal1
	bus.write_byte_data(address,0x13,newstate)

if (isodd(int(sys.argv[1])) == 0 and str(sys.argv[2]) == "amber2"):
	bus.write_byte_data(address,0x13,signal1)
	newstate = 128 + signal1
	bus.write_byte_data(address,0x13,newstate)
