class Signal(object):
    """A signal should dicate the movement of trains in the layout, there should be a maximum of two per section (one in each direction).

Constructor:
	Signal(id,section_id,placement,aspects) 
	
	id = Some identifier for the system
	gpio_in = The GPIO connector object the signal is associated with
	aspects = The number of aspects the signal has
	start_address = The first pin on the GPIO the RED signal is connected to, order HAS to be Red,Amber,Green,Amber,Feathers_1,Feathers_N... This means you can have multiple signals per GPIO! 
"""
    def __init__(self, id_in, gpio_in, aspects_in, start_address_in):
        """Method docstring."""
	self.id = id_in
        self.gpio = gpio_in
	self.aspects = aspects_in
	self.start_address = int(start_address_in)

    def getId(self):
	return self.id

    def getGPIO(self):
	return self.gpio

    def getAspects(self):
        """Method docstring."""
        return self.aspects
    
    def getPorts(self):
        """Method docstring."""
        return self.aspects

    def getStartAddress(self):
	return self.start_address
	
    def setColor(self,color):
	"""Returns the mask for the signal color, this has to be put together with other data before being sent to the bus"""
	if (color == "red"):
		mask = 0x01
	if (self.getAspects() == 2 and (color == "green" or color == "amber")):
		mask = 0x02
	if (self.getAspects() == 3 and color == "amber"):
		mask = 0x02
	if (self.getAspects() > 2 and color == "green"):
		mask = 0x04
	if (self.getAspects() == 4 and color == "twoamber"):
		mask = 0x0A
	self.mask = mask
	self.color = color	
	print "Setting ACTUAL signal " + self.getId() + " to " + str(mask)
	self.getGPIO().updateState()  
 
    def getColor(self):
	return self.color

    def getMask(self):
	return self.mask

    def setColorByCount(self,count):
	if (count == 0):
		self.setColor("red")
	if (self.getAspects() == 4 and count > 2):
		self.setColor("green")
	if (self.getAspects() == 4 and count == 2):
		self.setColor("twoamber")
	if (self.getAspects() == 3 and count > 1):
		self.setColor("green")
	if (self.getAspects() < 4 and count == 1):
		self.setColor("amber")
