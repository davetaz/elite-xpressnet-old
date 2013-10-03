import smbus

class PiInterface(object):
    """A simple bus like interface to as raspberry pi

Constructor:
	PiInterface(bus)
	
	bus: THe number of the usb bus the Pi is accesible on. You can thus have multiples! 

"""
    def __init__(self, bus_in):
        """Method docstring."""
	self.bus = smbus.SMBus(bus_in)

    def getBus():
	return self.bus
