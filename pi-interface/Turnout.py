from GenericOutput import Output
from time import sleep
import logging

class Turnout(Output):

    def __init__(self, id_in, gpio_in, pinOut_in, start_address_in):
	Output.__init__(self, id_in, gpio_in, pinOut_in, start_address_in)
	logging.debug("Initialising turnout " + str(id_in))
	self.position = "NULL"
	
    def setPosition(self,position):
	position_mask = self.getStartAddress()
	mask = 0
	bits = self.getPinOut().split(",")
	for bit in bits:
		logging.debug("Comparing " + bit + " to " + position)
		if (bit == position):
			self.position = position
			mask = mask + position_mask
		position_mask = position_mask << 1
		
	logging.debug("Setting ACTUAL turnout " + self.getId() + " to " + str(mask))
	self.setMask(mask)
	sleep(0.7)
	self.setMask(0)

    def getPosition(self):
	return self.position
