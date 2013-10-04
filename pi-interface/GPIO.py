class GPIO(object):
    """A gpio channel on an MCP23017, this class is designed to separate A from B bank and not be any more modular! 

Constructor:
	GPIO(Interface,address,bank,mode)
	
	Interface: An Interface which provides a getBus() method for commuicating with this GPIO channel.
	Address: The address of the mcp23017 chip (e.g. 32 or 0x20)
	Bank: The bank of GPIO pins (A or B)
	Mode: One of Input or Output for this whole Bank

For referece, here are the MCP23017 addresses for use:

IODIRA =  0x00 
IODIRB =  0x01
GPINTENA = 0X04
GPINTENB = 0x05
GPPUA  =  0x0c
GPPUB  =  0x0d
INTFA  =  0x0e
INTFB  =  0x0f
INTCAPA=  0x10
INTCAPB=  0x11
GPIOA  =  0x12
GPIOB  =  0x13

Modes:
Input = 0xff
Output = 0x00
"""

    def __init__(self, interface_in, address_in, bank_in, mode_in):
        """Method docstring."""
	self.interface = interface_in
	self.address = int(address_in)
	self.bank = bank_in
	if (self.bank == "A"): 
		self.IODIR = 0x00
		self.GPPU = 0x0c
		self.GPINTENA = 0x04
		self.INTCAP = 0x10
		self.GPIO = 0x12 
	if (self.bank == "B"):	
		self.IODIR = 0x01
		self.GPPU = 0x0d
		self.GPINTENA = 0x05
		self.INTCAP = 0x11
		self.GPIO = 0x13 
	self.mode = mode_in
	self.recordedState = 255
	if (self.mode == "intput"):
		try:
			self.interface.getBus().write_byte_data(self.address,self.IODIR,0xff)
		except:
			pass
		else:
			pass
	if (self.mode == "output"):
		self.signals = []
		try:
			self.interface.getBus().write_byte_data(self.address,self.IODIR,0x00)
		except:
			pass
		else: 
			pass

    def getInterface(self):
	return self.interface

    def getAddress(self):
	return self.address

    def getBank(self):
	return self.bank
	
    def getMode(self):
	return self.mode
  
    def getState(self):
	try:
		state = self.getInterface().getBus().read_byte_data(self.getAddress(),self.INTCAP);
	except:
		return "NULL"
	else:
		return int(state)
	
    def setState(self,state):
	try:
		self.getInterface().getBus().write_byte_data(self.getAddress(),self.GPIO,state)
	except: 
		print "Failed to set state"
	else:
		pass
	
    def setRecordedState(self,state):
	self.recordedState = state

    def getRecordedState(self):
	return self.recordedState

    def addSignal(self, signal):
        self.signals.append(signal)

    def getSignals(self):
        return self.signals
