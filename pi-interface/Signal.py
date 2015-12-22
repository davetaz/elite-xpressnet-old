from GenericOutput import Output

class Signal(Output):

    def __init__(self, id_in, gpio_in, pinOut_in, start_address_in,aspects_in):
	Output.__init__(self, id_in, gpio_in, pinOut_in, start_address_in)
	self.aspects = aspects_in
	
    def getAspects(self):
        """Method docstring."""
        return self.aspects
   
    def getColor(self):
	return self.color

    def setColor(self,color):
	"""Returns the mask for the signal color, this has to be put together with other data before being sent to the bus"""
	if (self.getAspects() == 2 and (color == "green" or color == "twoamber")):
		color = "amber"
	
	position_mask = self.getStartAddress()
	mask = 0
	bits = self.getPinOut().split(",")
	for bit in bits:
		if (bit == "R" and color == "red"):
			mask = mask + position_mask
		if (bit == "A" and (color == "amber" or color == "twoamber")):
			mask = mask + position_mask
		if (bit == "G" and color == "green"):
			logging.debug("Matched for green")
			mask = mask + position_mask
		if (bit == "2A" and color == "twoamber"):
			mask = mask + position_mask
		
		position_mask = position_mask << 1
		
	self.color = color	
	logging.debug("Setting ACTUAL signal " + self.getId() + " to " + str(mask))
	self.setMask(mask)
