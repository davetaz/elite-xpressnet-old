class Signal(object):
    """A signal should dicate the movement of trains in the layout, there should be a maximum of two per section (one in each direction).

Constructor:
	Signal(id,section_id,placement,aspects) 
	
	id = Some identifier for the system
	section_id = The id of the section the signal is in
	placement = The position of the signal in the section, their should be a maximum of 2 signals per section with one at the Forward (F) and one at the Reverse (R) end (if the Section is Bi-Directional! 
	aspects = The number of aspects the signal has
	redis = The reference to the redis library for handling messages
	action_queue = The message queue which events are pushed to in order to control the PHYSICAL signal, e.g. via a raspberry pi or other interface that consumes and processes these messages.

"""
    def __init__(self, id_in, section_id, placement, aspects, redis, action_queue):
        """Method docstring."""
	self.id = id_in
        self.sectionID = section_id
	self.placement = placement
	self.aspects = aspects
	self.redis = redis
	self.action_queue = action_queue

    def getId(self):
	return self.id

    def getRedisMQ(self):
	return self.redis
    
    def getActionQueue(self):
	return self.action_queue

    def getSectionID(self):
        """Method docstring."""
        return self.sectionID

    def getPlacement(self):
        """Method docstring."""
        return self.placement
    
    def getAspects(self):
        """Method docstring."""
        return self.aspects
	
    def setColor(self,color):
	"""Sets the signal color, supports: red,amber,green,twoamber. Feathers not yet implemented"""
	self.getRedisMQ().rpush(self.getActionQueue(),'"' + self.getId() + '",' + color);
	self.color = color	
    
    def getColor(self):
	return self.color

    def setColorByCount(self,count):
	if (count == 0):
		self.setColor("red")
	if (self.getAspects() == 4 and count > 2):
		self.setColor("green")
	if (self.getAspects() == 4 and count == 2):
		self.setColor("twoamber")
	if (self.getAspects() == 3 and count > 1):
		self.setColor("green")
	if (self.getAspects() < 4 and count == 1):
		self.setColor("amber")
