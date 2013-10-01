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
	
    def getSection(self, direction):
	if (direction == "F"):
		return self.getForwardSection()
	if (direction == "R"):
		return self.getReverseSection()

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
        if (self.getDirections() == "B" or self.getDirections() != direction):
		print "Setting direction for " + str(self.getId()) + " to " + direction
		self.currentDirection = direction
	
#"""FIXED: This should be based upon routing, not automatic"""
	
#In order to reverse the train automatically we need to look at the number of clear sections ahead of the new request (in the new direction) and compare this to the number of available sections (to end of route). 
# If the number of clear sections = number of sections or clear sections > 3, reverse the lot and ensure that red is showing in the opposite direction. 
# Update signals routine needs to take into account the direction of each section (which it might do already)
# If the number of clear sections < 2 and number of sections > 2, do nothing
	if (self.getNextSection()):
		clearSections = []
		connectedSections = []
		clearSections = self.getClearSectionsDirection(clearSections,direction)
		connectedSections = self.getSectionsDirection(connectedSections,direction)
		print "Clear Sections = " + str(len(clearSections))
		print "Connected Sections = " + str(len(connectedSections))
	
		if ((len(clearSections) == len(connectedSections)) or (len(clearSections) > 3)):
			
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

    def getSignal(self, direction):
	for signal in self.getSignals():
		if(signal.getPlacement() == direction):
			return signal

    def setSignalColor(self, direction, color):
	try:
		signal = self.getSignal(direction).setColor(color)
  	except: 
		pass

    def updateSignals(self):
	opposite = "F"
	if (self.currentDirection == "F"):
		opposite = "R"
	self.setSignalColor(opposite,"red")
	clearSectionCount = self.getClearCount(0)
	print "Section " + str(self.getId()) + " Count " + str(clearSectionCount)
	signal = self.getSignal(self.getCurrentDirection())
	if (signal):
		signal.setColorByCount(clearSectionCount)

    def setTrain(self, train):
	self.train = train

    def getTrain(self):
	try:
		self.train
	except: 
		pass
	else:
		return self.train

    def isOccupied(self):
	try:
		self.train
	except: 
		return 0
	else:
		return 1
	
    def getClearCount(self,count):
	nextSection = self.getNextSection()
	if (nextSection):
		if (nextSection.isOccupied()):
			return count
		else:
			count = count + 1
			return nextSection.getClearCount(count)
	else:
		return count

    def getSectionCount(self,count):
	nextSection = self.getNextSection()
	if (nextSection):
		count = count + 1
	else:
		return count
    
    def getSectionsDirection(self,connectedSections,direction):
	nextSection = self.getSection(direction)
	if (nextSection):
		connectedSections.append(nextSection)
		return nextSection.getSectionsDirection(connectedSections,direction)
	else:
		return connectedSections
	
    
    def getClearSectionsDirection(self,clearSections,direction):
	nextSection = self.getSection(direction)
	if (nextSection):
		if (nextSection.isOccupied()):
			return clearSections
		else:
			clearSections.append(nextSection)
			return nextSection.getClearSectionsDirection(clearSections,direction)
	else:
		return clearSections

