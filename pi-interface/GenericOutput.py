class Output(object):
    """A template for a generic output device (multi channel) that can have many ports etc

Constructor:
	Output(id,gpio,ports,start_address) 
	
	id = Some identifier for the system
	gpio = The GPIO connector object the output device is associated with
	ports = The number of ports the output is connected to on the GPIO
	start_address = The address of the first port
"""
    def __init__(self, id_in, gpio_in, pinOut_in, start_address_in):
        """Method docstring."""
	self.id = id_in
        self.gpio = gpio_in
	self.start_address = int(start_address_in)
	self.pinOut = pinOut_in

	bits = self.getPinOut().split(",")
	ports_in = len(bits)
	self.ports = ports_in

	# FIXME Read the mask from the GPIO so if the system creashes we don't need a total reset
	self.mask = self.getPhysicalMask()

    def getId(self):
	return self.id

    def getGPIO(self):
	return self.gpio

    def getPinOut(self):
	return self.pinOut
    
    def getPorts(self):
        """Method docstring."""
        return self.ports

    def getStartAddress(self):
	return self.start_address
	
    def setMask(self,mask_in):
	self.mask = mask_in
	self.getGPIO().updateState()  
   
    def getMask(self):
	return self.mask

    def getPhysicalMask(self):
	gpio_mask = self.getGPIO().getState()
	start = self.getStartAddress();
	# TODO HERE
	return 0;
