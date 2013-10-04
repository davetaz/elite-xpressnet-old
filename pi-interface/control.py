import json
import redis

# The Interfaces, this is the bit to change if you want to use a different interface library.
from PiInterface import PiInterface
from GPIO import GPIO
from Signal import Signal

json_data=open('../track/config.json')
data = json.load(json_data)
redis = redis.Redis()

pi = {}
gpio = {}
signal = {}

for pi_in in data["piinterface"]:
	pi[pi_in["id"]] = PiInterface(pi_in["bus"]);

for gpio_in in data["gpio"]:
	gpio[gpio_in["id"]] = GPIO(pi[gpio_in["pi_id"]],gpio_in["address"],gpio_in["bank"],gpio_in["mode"])
	print str(gpio_in["id"])

for s_in in data["signals"]:
	bits = s_in["id"].split(",")
	key = str(bits[0]) + "," + str(bits[1])
	io = gpio[key]
	start_address = bits[2]
	signal[s_in["id"]] = Signal(s_in["id"],io,s_in["aspects"],start_address)
       	io.addSignal(signal[s_in["id"]])

def setSignals(signal,redis):
	message = redis.lpop('signal_action')
	if (message):
		bits = message.split('",')
		long_id = bits[0].replace('"','',1);
		color = bits[1]
		signal[long_id].setColor(color)
		print long_id + " to " + color

def readInputs(gpio):
	for io_id in gpio:
		io = gpio[io_id]
		if (io.getMode() == "input"):
			state = io.getState()
			if (state == "NULL"):
				pass
			else:
				mask = 255
				back = mask - state
				if (back > 0 and back != io.getRecordedState()):
					io.setRecordedState(back)
					active = str(io.getAddress() ) + "," + io.getBank() + "," + str(back)
					print "sensors " + active
					redis.rpush("sensors",active)
				if (state == 255):
					io.setRecordedState(255)
	
while 1:
	readInputs(gpio)
	setSignals(signal,redis)

