class Sensor(object):
    """A sensor detects the presence of a train or part of a train in a section.

Constructor:
	Sensor(id,section_id,placement) 
	
	id = Some identifier for the system
	section_id = The id of the section the sensor is in
	placement = The position of the sensor in the section, their should be a maximum of 2 sensors per section with one at the Forward (F) and one at the Reverse (R) end.

"""

    def __init__(self, id_in, section_id, placement):
        """Method docstring."""
	self.id = id_in
        self.sectionID = section_id
	self.placement = placement

    def getId(self):
	return self.id

    def getSectionID(self):
        """Method docstring."""
        return self.sectionID

    def getPlacement(self):
        """Method docstring."""
        return self.placement
	
