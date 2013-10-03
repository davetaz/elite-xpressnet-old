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
	self.address = address_in
	self.bank = bank_in
	if (self.bank == "A"): 
		self.IODIR = 0x00
		self.GPPU = 0x0c
		self.GPINTENA = 0x04
	if (self.bank == "B"):	
		self.IODIR = 0x01
		self.GPPU = 0x0d
		self.GPINTENA = 0x05
	self.mode = mode_in
	if (self.mode == "intput"):
		self.interface.getBus().write_byte_data(self.address,self.IODIR,0xff)
	if (self.mode == "output"):
		self.interface.getBus().write_byte_data(self.address,self.IODIR,0x00)

    def getInterface():
	return self.interface
