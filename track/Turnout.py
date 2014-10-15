class Turnout(object):
    """A turnout is a representation of section that can change in layout as it is a point or something else. This file acts much like a signal as the state of a Turnout can physically change (unlike a Section).

Constructor:
	Turnout(id,section_id,placement,aspects) 
	
	id = Some identifier for the system
	section_id = The id of the section the signal is in
	redis = The reference to the redis library for handling messages
	action_queue = The message queue which events are pushed to in order to control the PHYSICAL signal, e.g. via a raspberry pi or other interface that consumes and processes these messages.

"""
    def __init__(self, id_in, section_id, redis, action_queue):
        """Method docstring."""
	self.id = id_in
        self.sectionID = section_id
	self.redis = redis
	self.action_queue = action_queue
	self.connected = 0

    def getId(self):
	return self.id

    def getRedisMQ(self):
	return self.redis
    
    def getActionQueue(self):
	return self.action_queue

    def getSectionID(self):
        """Method docstring."""
        return self.sectionID

    def setConnected(self,sectionNum):
	if (self.connected == sectionNum): 
		return
	self.getRedisMQ().rpush(self.getActionQueue(),'"' + self.getId() + '",' + str(sectionNum));
	self.connected = sectionNum	
    
    def getConnected(self):
	return self.connected
