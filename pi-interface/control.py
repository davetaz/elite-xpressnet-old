#!/usr/bin/env python
import logging
import json
import redis

LOG_FILENAME = "/home/pi/elite-xpressnet/pi-interface/run/log.txt"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode="w")

# The Interfaces, this is the bit to change if you want to use a different interface library.
from PiInterface import PiInterface
from GPIO import GPIO
from Signal import Signal
from Turnout import Turnout

json_data=open('/home/pi/elite-xpressnet/track/config.json')
data = json.load(json_data)
redis = redis.Redis()

pi = {}
gpio = {}
output = {}

for pi_in in data["piinterface"]:
	pi[pi_in["id"]] = PiInterface(pi_in["bus"]);

for gpio_in in data["gpio"]:
	gpio[gpio_in["id"]] = GPIO(pi[gpio_in["pi_id"]],gpio_in["address"],gpio_in["bank"],gpio_in["mode"])
	logging.debug(str(gpio_in["id"]))

for s_in in data["signals"]:
	bits = s_in["id"].split(",")
	key = str(bits[0]) + "," + str(bits[1])
	io = gpio[key]
	start_address = bits[2]
	output[s_in["id"]] = Signal(s_in["id"],io,s_in["pinOut"],start_address,s_in["aspects"])
	io.addOutput(output[s_in["id"]])


for t_in in data["turnouts"]:
	bits = t_in["id"].split(",")
	key = str(bits[0]) + "," + str(bits[1])
	io = gpio[key]
	start_address = bits[2]
	output[t_in["id"]] = Turnout(t_in["id"],io,t_in["pinOut"],start_address)
	io.addOutput(output[t_in["id"]])

def setSignals(output,redis):
	message = redis.lpop('signal_action')
	if (message):
		bits = message.split('",')
		long_id = bits[0].replace('"','',1);
		color = bits[1]
		output[long_id].setColor(color)
		logging.debug(long_id + " to " + color)

def setTurnouts(output,redis):
	message = redis.lpop('turnout_action')
	if (message):
		bits = message.split('",')
		long_id = bits[0].replace('"','',1);
		position = bits[1]
		output[long_id].setPosition(position)
		logging.debug(long_id + " to " + position)

def readInputs(gpio):
	for io_id in gpio:
		io = gpio[io_id]
		if (io.getMode() == "input"):
			state = io.getState()
#			logging.debug("Reading state " + str(state) + " from " + str(io_id));
			if (state == "NULL"):
				pass
			else:
				mask = 255
				back = mask - state
				if (back > 0 and back != io.getRecordedState()):
					io.setRecordedState(back)
					active = str(io.getAddress() ) + "," + io.getBank() + "," + str(back)
					logging.debug("sensors " + active)
					redis.rpush("sensors",active)
				if (state == 255):
					io.setRecordedState(255)
	
while 1:
	readInputs(gpio)
	setSignals(output,redis)
	setTurnouts(output,redis)

