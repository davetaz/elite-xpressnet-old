class Section(object):
    """A section is a piece of track between two signals on a track layout. Note that a section can ONLY be a strait section with two detention sensors and only forward or reverse directions. Turnouts (i.e. points) are a special type of section.

Constructor:
	Section(directions) 
	
	directions = Forward/Reverse/Bi-Directional as F/R/B

"""

    def __init__(self, id_in, directions, initialDirection):
        """Method docstring."""
	self.id = id_in
        self.directions = directions
	if (directions != "B"):
		self.currentDirection = directions
	else: 
		self.currentDirection = "F"
	if (initialDirection):
		self.currentDirection = initialDirection;
	self.sensors = []
	self.signals = []
	self.forwardSections = []
	self.reverseSections = []
	self.turnout = None
	self.isTurnout = False
	self.maxSpeed = 0

    def getId(self):
	return self.id

    def getDirections(self):
        """Method docstring."""
        return self.directions

    def setDirections(self, directions):
        """Method docstring."""
        self.directions = directions
	
    def getSection(self, direction):
#	print "retrieving next section to " + str(self.getId()) + " in direction " + direction
	if (direction == "F"):
		return self.getForwardSection()
	if (direction == "R"):
		return self.getReverseSection()

    def setTurnout(self, turnout):
#	print "setting turnout for section " + str(self.getId())
	self.turnout = turnout 

    def getTurnout(self):
	return self.turnout

    def setForwardSection(self, section):
	self.forwardSections.append(section)
    
    def setCurrentForwardSection(self, section):
	self.forwardSection = section
   
    def getCurrentForwardSectionId(self):
	try:
		self.forwardSection
	except:
		return
	else:
		return self.forwardSection.getId();
 
    def getForwardSection(self):
	try: 
		self.forwardSection
	except: 
		pass
	else: 
		return self.forwardSection
    
    def getForwardSections(self):
	return self.forwardSections;
    
    def setReverseSection(self, section):
	self.reverseSections.append(section)

    def setCurrentReverseSection(self, section):
	self.reverseSection = section
    
    def getCurrentReverseSectionId(self):
	try:
		self.reverseSection
	except:
		return
	else:
		return self.reverseSection.getId();
    
    def getReverseSection(self):
	try:
		self.reverseSection
	except:
		pass
	else: 
		return self.reverseSection
		
    def getReverseSections(self):
	return self.reverseSections;

    def setTurnoutSection(self,state):
	self.isTurnout = state

    def getTurnoutSection(self):
	return self.isTurnout

    def autoConnectSections(self):
	if (len(self.getForwardSections()) > 1 or len(self.getReverseSections()) > 1):
		self.setTurnoutSection(True)
	if (len(self.getReverseSections()) == 1):
		prev_section = self.getReverseSections()[0]
#		print "[TURNOUT] Connecting section " + str(self.getId()) + " to section " + str(prev_section.getId());
		self.setCurrentReverseSection(prev_section)
	else:
		for prev_section in self.getReverseSections():
			if (prev_section.getCurrentDirection() == self.getCurrentDirection()):
#				print "[NEED TO SET TURNOUT] connecting section " + str(self.getId()) + " to section " + str(prev_section.getId());
				self.getTurnout().setConnected(prev_section.getId());
				self.setCurrentReverseSection(prev_section)
	if (len(self.getForwardSections()) == 1):
		next_section = self.getForwardSections()[0]
#		print "connecting section " + str(self.getId()) + " to section " + str(next_section.getId());
		self.setCurrentForwardSection(next_section)
	else:
		for next_section in self.getForwardSections():
			if (next_section.getCurrentDirection() == self.getCurrentDirection()):
#				print "[NEED TO SET TURNOUT] connecting section " + str(self.getId()) + " to section " + str(next_section.getId());
				self.getTurnout().setConnected(next_section.getId());
				self.setCurrentForwardSection(next_section)
	
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
#	print ""
#	print "Trying to set direction of section " + str(self.getId()) + " to " + direction 
	nextSection = self.getNextSection();
	if (nextSection):
#		if (self.getDirections() == "B" and self.getTurnoutSection() == False and (nextSection.getDirections() == "B" or nextSection.getDirections() == direction)):
		if (self.getTurnoutSection() == False):
#			print "[NO TURNOUT] Setting direction for " + str(self.getId()) + " to " + direction
			self.currentDirection = direction
		if (self.getDirections() == "B" and self.getTurnoutSection() == True):
#			print "[TURNOUT] Need to autoconnect to the right section"
			self.currentDirection = direction
			self.autoConnectSections()
			nextSection = self.getNextSection()
			nextSection.setCurrentDirection(direction)
	else:
		if (self.getDirections() == "B" and self.getTurnoutSection() == False):
#			print "NO TURNOUT Setting direction for " + str(self.getId()) + " to " + direction
			self.currentDirection = direction
	
	

	nextSection = self.getNextSection();
	if (nextSection):
		clearSections = []
		connectedSections = []
		if (nextSection.getCurrentDirection() != self.getCurrentDirection()):
			clearSections = nextSection.getClearSectionsDirection(clearSections,direction)
			connectedSections = nextSection.getSectionsDirection(connectedSections,direction)
#			print "Clear Sections = " + str(len(clearSections))
#			print "Connected Sections = " + str(len(connectedSections))
			if ((len(clearSections) == len(connectedSections)) or (len(clearSections) > 3)):	
				nextSection.setCurrentDirection(direction)
	
#"""FIXED: This should be based upon routing, not automatic"""
	
#In order to reverse the train automatically we need to look at the number of clear sections ahead of the new request (in the new direction) and compare this to the number of available sections (to end of route). 
# If the number of clear sections = number of sections or clear sections > 3, reverse the lot and ensure that red is showing in the opposite direction. 
# Update signals routine needs to take into account the direction of each section (which it might do already)
# If the number of clear sections < 2 and number of sections > 2, do nothing
	if (nextSection):
		clearSections = []
		connectedSections = []
		clearSections = self.getClearSectionsDirection(clearSections,direction)
		connectedSections = self.getSectionsDirection(connectedSections,direction)
#		print "Clear Sections = " + str(len(clearSections))
#		print "Connected Sections = " + str(len(connectedSections))
	
		if ((len(clearSections) == len(connectedSections)) or (len(clearSections) > 1)):	
			nextSection.setCurrentDirection(direction)
	else:
		return
#		print "NO NEXT SECTION!"	
	

    def getCurrentDirection(self):
        """Get current direction of section"""
        return self.currentDirection

    def setMaxSpeed(self, speed):
        """Method docstring."""
        self.maxSpeed = speed
    
    def getMaxSpeed(self):
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

    def setSectionSpeed(self):
	clearSections = []
	self.setMaxSpeed(len(self.getAllClearSectionsDirection(clearSections,self.currentDirection)))
#	print "setting max speed of section " + str(self.getId()) + " to " + str(self.getMaxSpeed())

    def updateSignals(self):
	clearSections = []
	self.setMaxSpeed(len(self.getAllClearSectionsDirection(clearSections,self.currentDirection)))
	if (len(self.getSignals()) < 1):	
		return
	opposite = "F"
	if (self.currentDirection == "F"):
		opposite = "R"
	self.setSignalColor(opposite,"red")
	clearSections = []
	clearSections = self.getClearSectionsDirection(clearSections,self.currentDirection)
	clearSectionCount = len(clearSections)
#	print "Section " + str(self.getId()) + " Count " + str(clearSectionCount)
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
		if (nextSection.getTurnoutSection() == False):
			connectedSections.append(nextSection)
		return nextSection.getSectionsDirection(connectedSections,direction)
	else:
		return connectedSections
    
    def getAllClearSectionsDirection(self,clearSections,direction):
#	print "Getting all clear sections for section " + str(self.getId()) + " has clearsections " + str(len(clearSections)) + " in direction " + direction
	nextSection = self.getSection(direction)
	signal = self.getSignal(direction)
	try:
		if signal.getColor() == "red":
			return clearSections
	except:
		pass
	if (nextSection):
#		print "checking section " + str(nextSection.getId())
		if (nextSection.isOccupied() or (nextSection.getCurrentDirection() != self.getCurrentDirection())):
			return clearSections
		else:
			clearSections.append(nextSection)
#			print ("Appeded " + str(nextSection.getId()) + " count " + str(len(clearSections)))
			return nextSection.getAllClearSectionsDirection(clearSections,direction)
	else:
#		print "No next section!"
		return clearSections

    def getClearSectionsDirection(self,clearSections,direction):
#	print "Getting clear sections for section " + str(self.getId()) + " has clearsections " + str(len(clearSections)) + " in direction " + direction
	nextSection = self.getSection(direction);
	if (nextSection):
#		print "checking section " + str(nextSection.getId())
		if (nextSection.isOccupied() or (nextSection.getCurrentDirection() != self.getCurrentDirection())):
			return clearSections
		else:
			if (nextSection.getTurnoutSection() == False):
				clearSections.append(nextSection)
#				print ("Appeded " + str(nextSection.getId()) + " count " + str(len(clearSections)))
			return nextSection.getClearSectionsDirection(clearSections,direction)
	else:
#		print "No next section!"
		return clearSections
