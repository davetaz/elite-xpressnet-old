import json
import redis
from Section import Section
from Sensor import Sensor
from Signal import Signal
from Train import Train

json_data=open('config.json')
data = json.load(json_data)

section = {}
sensor = {}
signal = {}
train = {}

# Set up Sections
for s_in in data["sections"]:
	section[s_in["id"]] = Section(s_in["id"],s_in["directions"])

# Iterate over the sections in the config to set next and previous
for s_in in data["sections"]:
	try:
		s_in["forward"] and section[s_in["forward"]]
	except:
		pass
#		print "Caught forward exception with section " + str(s_in["id"])
	else:
		section[s_in["id"]].setForwardSection(section[s_in["forward"]])
	try: 
		s_in["reverse"] and section[s_in["reverse"]]
	except:
		pass
#		print "Caught reverse exception with section " + str(s_in["id"])	
	else:
		section[s_in["id"]].setReverseSection(section[s_in["reverse"]])
		
# Setup sensors and add these to sections
for s_in in data["sensors"]:
	sensor[s_in["id"]] = Sensor(s_in["id"],section[s_in["section"]],s_in["placement"])
	section[s_in["section"]].addSensor(sensor[s_in["id"]])

# Setup signals and add these to sections
for s_in in data["signals"]:
	signal[s_in["id"]] = Signal(s_in["id"],s_in["section"],s_in["placement"],s_in["aspects"])
	signal[s_in["id"]].setColor("red")
	section[s_in["section"]].addSignal(signal[s_in["id"]])

# Setup train locations, adding sections as references
for t_in in data["trains"]:
	train[t_in["id"]] = Train(t_in["id"],t_in["sensor_count"])
	for sec_in in t_in["sections"]:
		train[t_in["id"]].addSection(section[sec_in])
		section[sec_in].setTrain(train[t_in["id"]])
	
#print section[1].getCurrentDirection();

#Get Train #3
t_3 = train[3];
#Get the sections that Train #3 is currently in
sections = t_3.getSections();
for section in sections:
	#Get the signals in this section
	print "Current Section = " + str(section.getId()) + " direction = " + section.getCurrentDirection()
	nextSection = section.getNextSection()	
	try:
		nextSection
	except:
		print "No next section!";
	else:
		print "Next Section: " + str(nextSection.getId())

	s_1 = section.getSignals();
	#Print out some info
	for s in s_1:
		print s.getId() 
		print s.getPlacement()
		print s.getColor()


# TASK 1
# Follow a train along a number of sections
# Consume events from the queue and send events to the queue to set signals potentially

r = redis.Redis()

# TODO Need to work out how to reverse, perhaps autoreverse if in a bi directional section and there is no further section

while 1:
	message = r.lpop('sensors')
	if (message):
		bits = message.split(',')
		address = bits[0] + "," + bits[1]
		lsensor = sensor[address]
		lsensor.triggerCount += 1
		lsection = lsensor.getSection()
		train = lsection.getTrain()
		print "Sensor activated: " + address + " Section: " + str(lsection.getId()) + " Direction: " + lsensor.getPlacement() + " Count " + str(lsensor.triggerCount)
		if (lsensor.triggerCount % 2 == 0 and lsection.getPreviousSection()):
			prevSection = lsection.getPreviousSection()
			try:
				prevSection.train
			except: 
				pass
			else:
				del prevSection.train
				for tsensor in prevSection.getSensors():
					tsensor.triggerCount = 0 
				print "Train has left Section " + str(lsection.getPreviousSection().getId())
		if (lsensor.triggerCount % 2 == 0):
			lsensor.triggerCount = 0
		if (train):
			print "Train " + str(train.getId()) + " in section already"
		else:
			print "Need to work out which train this is!"
			train = lsection.getPreviousSection().getTrain()
			if (train): 
				print "Train " + str(train.getId()) + " moved from Section " + str(lsection.getPreviousSection().getId()) + " to section " + str(lsection.getId())
				lsection.setTrain(train)
			
#		lsection = section[lsensor.getSectionId()]
#		print "Sensor activated: " + address + " Section: " + lsection.getId() + " Direction: " + lsensor.getPlacement

# TASK 2
# Set a signal to allow a train into the next section
# 1. Find the signal and direction
# 2. Begin itterator to find number of clear sections, up to 3 sections max. 
	# A. Get the next section in the direction of the signal, check if any trains are in the section
	# B. If clear, Find the reverse signal in the next (2 along) section and set it to stop (it should also check that it can be set to stop by checking that there are no trains in the section heading towards it).
# 4. Set the signal to clear with the color that represents the number of sections that are clear ahead. 

