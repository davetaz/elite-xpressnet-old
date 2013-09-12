class Section(object):
    """A section is a piece of track between two signals on a track layout. Note that a section can ONLY be a strait section with two detention sensors and only forward or reverse directions. Turnouts (i.e. points) are a special type of section.

Constructor:
	Section(directions) 
	
	directions = Forward/Reverse/Bi-Directional as F/R/B

"""

    def __init__(self, id_in, directions):
        """Method docstring."""
	self.id = id_in
        self.directions = directions
	if (directions != "B"):
		self.currentDirection = directions
	else: 
		self.currentDirection = "F"
	self.sensors = []
	self.signals = []

    def getId(self):
	return self.id

    def getDirections(self):
        """Method docstring."""
        return self.directions

    def setDirections(self, directions):
        """Method docstring."""
        self.directions = directions
	
    def setForwardSection(self, section):
	self.forwardSection = section
    
    def getForwardSection(self):
	try: 
		self.forwardSection
	except: 
		pass
	else: 
		return self.forwardSection
    
    def setReverseSection(self, section):
	self.reverseSection = section
    
    def getReverseSection(self):
	try:
		self.reverseSection
	except:
		pass
	else: 
		return self.reverseSection
		

    def getNextSection(self):
	if (self.getCurrentDirection() == "F"):
		return self.getForwardSection()
	if (self.getCurrentDirection() == "R"):
		return self.getReverseSection()
    
    def getPreviousSection(self):
	if (self.getCurrentDirection() == "R"):
		return self.getForwardSection()
	if (self.getCurrentDirection() == "F"):
		return self.getReverseSection()

    def setCurrentDirection(self, direction):
        """Checks to see if section direction can be changed!"""
        if (self.getDirections() == "B" or self.getDirections() == direction):
		print "Setting direction for " + str(self.getId()) + " to " + direction
		self.currentDirection = direction
	
	"""FIXME: This should be based upon routing, not automatic"""
	if (self.getNextSection()):
		print "Trying to set direction for next section"
		self.getNextSection().setCurrentDirection(direction)

    def getCurrentDirection(self):
        """Get current direction of section"""
        return self.currentDirection

    def setMaxSpeed(self, speed):
        """Method docstring."""
        self.maxSpeed = speed
    
    def getMaxSpeed(self, speed):
        """Method docstring."""
        return self.maxSpeed

    def addSensor(self, sensor):
	self.sensors.append(sensor)

    def getSensors(self):
	return self.sensors
    
    def addSignal(self, signal):
	self.signals.append(signal)

    def getSignals(self):
	return self.signals

    def setTrain(self, train):
	self.train = train

    def getTrain(self):
	try:
		self.train
	except: 
		pass
	else:
		return self.train

