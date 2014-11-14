class Train(object):
    """A train in the system

Constructor:
	Train(id,sensor_count,sections) 
	
	id = Some identifier for the system
	sensor_count = The number of sensors on the train
	sections = The section or sections the train is currently ocupying with at least one sensor.

"""
    def __init__(self, id_in, sensor_count, speeds,redis,action_queue):
        """Method docstring."""
	self.id = id_in
        self.sensorCount = sensor_count
	self.speeds = speeds
	self.redis = redis
	self.action_queue = action_queue
	self.sections = []
	self.currentSpeed = 0
	self.direction = "f"

    def getRedisMQ(self):
	return self.redis
    
    def getActionQueue(self):
	return self.action_queue


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

    def getSpeedsArray(self):
	return self.speeds

    def addSection(self,section):
	self.sections.append(section)
	self.autoSetSpeed()
	
    def removeSection(self,section):
	self.sections.remove(section)
	self.autoSetSpeed()

    def autoSetSpeed(self):
	clearSections = 0
	actualSpeed = 0
	lastSection = False
	for section in self.sections:
		section.setSectionSpeed()
		if section.getMaxSpeed() > clearSections:
			clearSections = section.getMaxSpeed()
		nextSection = section.getNextSection()
		try:
			sectionId = nextSection.getId()
		except:
			if len(self.sections) == 1:
				lastSection = True
	try:
		actualSpeed = self.speeds[clearSections]
	except: 
		if len(self.speeds) <= clearSections:
			actualSpeed = self.speeds[len(self.speeds)-1]
		else:
			actualSpeed = 0;
	if lastSection:
		print "LAST SECTION: STOP!!!"
		self.setSpeed(0);
	else:		
		self.setSpeed(actualSpeed);
		print "Still moving: Setting max speed " + str(actualSpeed) + " clear sections " + str(clearSections)

    def setSpeed(self,speed):
	self.getRedisMQ().rpush(self.getActionQueue(),'"' + str(self.getId()) + '","' + self.getDirection() + '","'+ str(speed) + '"');
	self.currentSpeed = speed

    def getSpeed(self):
	return self.currentSpeed
    
    def setDirection(self,direction):
	try: 
		self.direction
	except:
		self.direction = direction

	if (self.direction == direction):
		return
	elif (self.currentSpeed == 0):
		self.direction = direction

    def getDirection(self):
	return self.direction


