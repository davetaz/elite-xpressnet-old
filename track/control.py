# Status update 22/9/2013 
# This simple example should now work with 3 connected sections, 4 sensors and 2 signals. This code needs freezing and testing at version 1. Then it could probably do with some tidying up with debug routines before moving onto adding turnouts.

import json
import redis
from Section import Section
from Sensor import Sensor
from Signal import Signal
from Train import Train
from Turnout import Turnout

json_data=open('config.json')
data = json.load(json_data)
redis = redis.Redis()

sections = {}
section = {}
turnout = {}
sensor = {}
signal = {}
train = {}

# Set up Sections
for s_in in data["sections"]:
	try:
		s_in["currentDirection"]
	except:
		s_in["currentDirection"] = False
	section[s_in["id"]] = Section(s_in["id"],s_in["directions"],s_in["currentDirection"])
	sections[section[s_in["id"]]] = 1

for s_in in data["turnouts"]:
	turnout[s_in["id"]] = Turnout(s_in["id"],s_in["section"],redis,"turnout_action")
	section[s_in["section"]].setTurnout(turnout[s_in["id"]])

# Iterate over the sections in the config to set next and previous, which is ALSO an ITTERATION!
# This does not define which section is connected!
for s_in in data["sections"]:
	try:
		s_in["forward"]
	except:
		pass
	else:
		for f_option in s_in["forward"]:
			section[s_in["id"]].setForwardSection(section[f_option])
	try:
		s_in["reverse"]
	except:
		pass
	else:
		for r_option in s_in["reverse"]:
			section[s_in["id"]].setReverseSection(section[r_option])

sec_buffer = [];
for s in section:
	if (len(section[s].getForwardSections()) > 1 or len(section[s].getReverseSections()) > 1):
		sec_buffer.append(section[s])
	else:
		section[s].autoConnectSections()
for s in sec_buffer:
	s.autoConnectSections()	
	
# Setup sensors and add these to sections
for s_in in data["sensors"]:
	sensor[s_in["id"]] = Sensor(s_in["id"],section[s_in["section"]],s_in["placement"])
	section[s_in["section"]].addSensor(sensor[s_in["id"]])

# Setup signals and add these to sections
for s_in in data["signals"]:
	signal[s_in["id"]] = Signal(s_in["id"],s_in["section"],s_in["placement"],s_in["aspects"],redis,"signal_action")
	try:
		s_in["color"] != ""
		signal[s_in["id"]].setColor(s_in["color"])
	except:
		signal[s_in["id"]].setColor("red")
	section[s_in["section"]].addSignal(signal[s_in["id"]])

# Setup train locations, adding sections as references
for t_in in data["trains"]:
	train[t_in["id"]] = Train(t_in["id"],t_in["sensor_count"],t_in["speeds"],redis,"traincon")
	for sec_in in t_in["sections"]:
		train[t_in["id"]].addSection(section[sec_in])
		section[sec_in].setTrain(train[t_in["id"]])
	
## TRAINING / DEBUG CODE 
## Performs some very basic operations
## print section[1].getCurrentDirection();
## Get Train #3
#t_3 = train[3];
## Get the sections that Train #3 is currently in
#tsections = t_3.getSections();
#for section in tsections:
## Get the signals in this section
#	print "Current Section = " + str(section.getId()) + " direction = " + section.getCurrentDirection()
#	nextSection = section.getNextSection()	
#	try:
#		nextSection
#	except:
#		print "No next section!";
#	else:
#		print "Next Section: " + str(nextSection.getId())
#
#	s_1 = section.getSignals();
## Print out some info
#	for s in s_1:
#		print s.getId() 
#		print s.getPlacement()
#		print s.getColor()
#

def updateSignals():
	global sections
	for s in sections:
#		print "Processing section " + str(s.getId())
		s.updateSignals()
			
# TASK 1
# Follow a train along a number of sections
# Consume events from the queue and send events to the queue to set signals potentially

def handleSensorUpdate(message,sensor):
	print ""
	print ""
	sensor.triggerCount += 1
	section = sensor.getSection()
	train = section.getTrain()
	print "Sensor activated: " + address + " Section: " + str(section.getId()) + " Placement: " + sensor.getPlacement() + " Count: " + str(sensor.triggerCount)
#	if sensor.getPlacement() == section.getCurrentDirection() and train:
#		nextSection = section.getNextSection()
#		signal = section.getSignal(section.getCurrentDirection())
#		try: 
#			sectionId = nextSection.getId()
#		except:
#			print "At the end of the line, NEED TO STOP"
#			train.setSpeed(0);
#		try:
#			if signal.getColor() == "red" and sensor.triggerCount % 2 > 0:
#				train.setSpeed(0);
#				print "RED SIGNAL STOP"
#		except:
#			pass
	if (train):
		print "Train: " + str(train.getId())
	else:
		print "No train in section " + str(section.getId())
	if (sensor.triggerCount % 2 == 0 and section.getPreviousSection()):
		prevSection = section.getPreviousSection()
		try:
			prevSection.train
		except: 
			pass
		else:
			del prevSection.train
			if (train):
				train.removeSection(prevSection)
			for psensor in prevSection.getSensors():
				psensor.triggerCount = 0		
		
			print "Train has left Section " + str(section.getPreviousSection().getId())
#			Call refresh on all signals
			updateSignals()

	if (sensor.triggerCount % 2 == 0):
		sensor.triggerCount = 0
	
	if (train):
		print "Train " + str(train.getId()) + " in section already"
		train.autoSetSpeed()
	else:
#		print "Need to work out which train this is!"
#		if (section.getPreviousSection()):
		train = section.getPreviousSection().getTrain()
		if (train):
#			print "It's train " + str(train.getId()) 
			section.setTrain(train)
			train.addSection(section)
			train.setDirection(section.getCurrentDirection())
			# Need to update signals
			prevSection = section.getPreviousSection()
			try:
				prevSection.getSignal(prevSection.getCurrentDirection()).setColor("red")
			except:
				pass
			updateSignals()
			train.autoSetSpeed()
			print "Train " + str(train.getId()) + " moved from Section " + str(section.getPreviousSection().getId()) + " to section " + str(section.getId()) + " in direction " + train.getDirection() + " new max speed = " + str(section.getMaxSpeed());
	if sensor.getPlacement() == section.getCurrentDirection() and train:
		nextSection = section.getNextSection()
		signal = section.getSignal(section.getCurrentDirection())
		try: 
			sectionId = nextSection.getId()
		except:
			print "At the end of the line, NEED TO STOP"
			train.setSpeed(0);
		try:
			if signal.getColor() == "red" and sensor.triggerCount % 2 > 0:
				train.setSpeed(0);
				print "RED SIGNAL STOP"
		except:
			pass


# Task 2: Handle train reverse instruction and call for section updates (Need to work out how to reverse, perhaps autoreverse if in a bi directional section and there is no further section)

def handleTrainUpdate(message,train,instruction,data):
	print ""
	print "" 
	if (instruction == "Direction"):
		sections = train.getSections()
		can_change = True
		for section in sections:
			if (section.getDirections() != "B" and section.getDirections() != data):
				can_change = False
		if can_change:
			for section in sections:
				section.setCurrentDirection(data)
			train.setDirection(data)
	updateSignals()
	train.autoSetSpeed()

def handleSignalUpdate(message,signal,mode,color):
	print ""
	print ""
	# Get the mode and set it, if different
	# Get the color and call see if it is different,
	# If it is different, see if it can be changed to this color:
		# Get number of clear sections forward (connected sections also)
		# Get number of clear sections reverse (connected sections also)
		# Set the color
	# If the signal is not in auto mode and is red, it remains red. Else it is set automatically (with auto mode still off).
	# The test is to set the second signal to auto off and set it to red, then call update signals and the previous one should be amber and not green.

def rewriteConfig(data):
	for t_in in data["trains"]:
		t_in["sections"] = train[t_in["id"]].getSectionsArray()
		t_in["direction"] = train[t_in["id"]].getDirection()
		t_in["speed"] = train[t_in["id"]].getSpeed()
		t_in["speeds"] = train[t_in["id"]].getSpeedsArray()

	for s_in in data["signals"]:
		s_in["color"] = signal[s_in["id"]].getColor()

	for s_in in data["sections"]:
		s_in["currentForwardSection"] = section[s_in["id"]].getCurrentForwardSectionId()
		s_in["currentReverseSection"] = section[s_in["id"]].getCurrentReverseSectionId()
		s_in["currentDirection"] = section[s_in["id"]].getCurrentDirection()
		s_in["currentMaxSpeed"] = section[s_in["id"]].getMaxSpeed()

	for t_in in data["turnouts"]:
		t_in["connected"] = turnout[t_in["id"]].getConnected()
		
	with open('config.json', 'w') as outfile:
		json.dump(data, outfile,indent=4)

updateSignals()

while 1:
	message = redis.lpop('sensors')
	if (message):
		print "Got a message " + message;
		bits = message.split(',')
		address = bits[0] + "," + bits[1] + "," + bits[2]
		try: 
			sensor[address]
		except:
			print "Recieved a message from a sensor that didn't exist in the config!"
			pass
		else: 
			handleSensorUpdate(message,sensor[address])
			rewriteConfig(data)
	
	message = redis.lpop('trains')
	if (message):
		bits = message.split(',')
		address = int(bits[0])
		instruction = bits[1]
		datablob = bits[2]
		try: 
			train[address]
		except:
			pass
		else: 
			handleTrainUpdate(message,train[address],instruction,datablob)
			rewriteConfig(data)
	
	message = redis.lpop('signals')

	if (message):
		bits = message.split(',')
		address = int(bits[0])
		mode = bits[1]
		color = bits[2]
		try: 
			signal[address]
		except:
			pass
		else: 
			handleSignalUpdate(message,signal[address],mode,color)
			rewriteConfig(data)

