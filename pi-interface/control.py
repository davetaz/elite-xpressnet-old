import json
import redis

# The Interfaces, this is the bit to change if you want to use a different interface library.
from PiInterface import PiInterface
from GPIO import GPIO

json_data=open('../track/config.json')
data = json.load(json_data)
redis = redis.Redis()

pi = {}
gpio = {}

for pi_in in data["piinterface"]:
	pi[pi_in["id"]] = PiInterface(pi_in["bus"]);

for gpio_in in data["gpio"]:
	gpio[gpio_in["id"]] = GPIO(pi[gpio_in["pi_id"]],gpio_in["address"],gpio_in["bank"],gpio_in["mode"]);
	
# TODO Hack the signal id's to associate them to gpio's, same with turnouts eventually. 
#for signal in data["signals"]:

