from GenericOutput import Output
from time import sleep

class Turnout(Output):

    def __init__(self, id_in, gpio_in, pinOut_in, start_address_in):
	Output.__init__(self, id_in, gpio_in, pinOut_in, start_address_in)
	print "Initialising turnout " + str(id_in)
	self.position = "NULL"
	
    def setPosition(self,position):
	position_mask = self.getStartAddress()
	mask = 0
	bits = self.getPinOut().split(",")
	for bit in bits:
		print "Comparing " + bit + " to " + position
		if (bit == position):
			self.position = position
			mask = mask + position_mask
		position_mask = position_mask << 1
		
	print "Setting ACTUAL turnout " + self.getId() + " to " + str(mask)
	self.setMask(mask)
	sleep(0.7)
	self.setMask(0)

    def getPosition(self):
	return self.position
