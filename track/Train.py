class Train(object):
    """A train in the system

Constructor:
	Train(id,sensor_count,sections) 
	
	id = Some identifier for the system
	sensor_count = The number of sensors on the train
	sections = The section or sections the train is currently ocupying with at least one sensor.

"""
    def __init__(self, id_in, sensor_count):
        """Method docstring."""
	self.id = id_in
        self.sensorCount = sensor_count
	self.sections = []
	self.speed = 0
	self.direction = "f"

    def getId(self):
	return self.id

    def getSensorCount(self):
        """Method docstring."""
        return self.sensorCount

    def getSections(self):
        """Method docstring."""
        return self.sections

    def getSectionsArray(self):
	array = []
	for section in self.sections:
		array.append(section.getId())
	return array

    def addSection(self,section):
	self.sections.append(section)
	
    def removeSection(self,section):
	self.sections.remove(section)

    def setSpeed(self,speed):
	self.speed = speed

    def getSpeed(self):
	return self.speed
    
    def setDirection(self,direction):
	try: 
		self.direction
	except:
		self.direction = direction

	if (self.direction == direction):
		return
	elif (self.speed == 0):
		self.direction = direction

    def getDirection(self):
	return self.direction


