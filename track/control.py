import json;
from Section import Section;
from Sensor import Sensor;
from Signal import Signal;
from Train import Train;

json_data=open('config.json');
data = json.load(json_data);

section = {}
sensor = {}
signal = {}
train = {}

for s_in in data["sections"]:
	section[s_in["id"]] = Section(s_in["id"],s_in["directions"]);

# TODO: Iteration over the sections in the config to set next and previous

for s_in in data["sensors"]:
	sensor[s_in["id"]] = Sensor(s_in["id"],section[s_in["section"]],s_in["placement"]);
	section[s_in["section"]].addSensor(sensor[s_in["id"]]);

for s_in in data["signals"]:
	signal[s_in["id"]] = Signal(s_in["id"],s_in["section"],s_in["placement"],s_in["aspects"]);
	signal[s_in["id"]].setColor("red")
	section[s_in["section"]].addSignal(signal[s_in["id"]]);

for t_in in data["trains"]:
	train[t_in["id"]] = Train(t_in["id"],t_in["sensor_count"])
	for sec_in in t_in["sections"]:
		train[t_in["id"]].addSection(section[sec_in])
	
#print section[1].getCurrentDirection();

#Get Train #3
t_3 = train[3];
#Get the sections that Train #3 is currently in
sections = t_3.getSections();
for section in sections:
	#Get the signals in this section
	s_1 = section.getSignals();
	#Print out some info
	for s in s_1:
		print s.getId() 
		print s.getPlacement()
		print s.getColor()

# TASK 1
# Set a signal to allow a train into the next section
# 1. Find the signal and direction
# 2. Begin itterator to find number of clear sections, up to 3 sections max. 
	# A. Get the next section in the direction of the signal, check if any trains are in the section
	# B. If clear, Find the reverse signal in the next (2 along) section and set it to stop (it should also check that it can be set to stop by checking that there are no trains in the section heading towards it).
# 4. Set the signal to clear with the color that represents the number of sections that are clear ahead. 

