# Use heSensor.py as the interface for train detection
# see heSensor.py for information on using this module.
import heSensor

#Use python standard module time for simple timming functions 
import time

# example functions for South West Digital's Class 108 (55488) decoder

# Enable the I2C bus between the Rpi and the sensor controller(s)
# see heSensor.py for information
heSensor.i2Cbus_open()
# Configure the sensor controller(s) - call heSensor for each controller on the bus
# see heSensor.py for information
heSensor.config(0x20)

# create a sensor object to represent each sensor on the track
# parameter 1 = address of controller
# parameter 2 = which of the two banks on the controller the sensor is connected to (A or B)
# parameter 3 = which of the ports on the controller the sensor is connected to (1 to 8)
s1 = heSensor.Sensor(0x20,'A',1)
s1.wait();
s2 = heSensor.Sensor(0x20,'A',2)
s2.wait();
