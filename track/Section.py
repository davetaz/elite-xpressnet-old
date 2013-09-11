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
    
    def setCurrentDirection(self, direction):
        """TODO: Add checks to see if section direction can be changed!"""
        self.currentDirection = direction

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

	
