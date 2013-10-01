# Track Control

Automatic or semi-automatic control of simple rail layouts.

This library is built to read in sensor data and control signals, turnouts and trains in order to allow automatic or semi-automatic controll of simple rail layouts. 

## Objects

The library is developed in python and uses a number of classes to represent the objects in a railway layout:

* Train.py - Allows control of a train, speed and DCC functions.
* Sensor.py - Some form of sensor that gets activated when a train passes over it or activates it. Used to find the possition of the trains.
* Signal.py - A signal, position, colour and direction of control. 
* Section.py - Defines a section of train, this is the key class as a section may contain many Sensors,Signals and Trains.
	
For more information on each class, usage and API please refer to the comments in each.

## Defining a layout

A layout is defined in the config.json file. 

The example layout consists of:
	* 3 Sections
	* 6 Sensors
	* 4 Signals
	* 1 Train

This layout defines a strait piece of track with no turnouts (points) that a train can travel from one end to the other and back. There are three sections with two sensors in each, one at each end of the section. Similarly there are four signals located between sections 1 and 2 and between sections 2 and 3, one in each direction.

In diagramatic form:

###Key
* |----------------| = Section
* X = Sensor
* } = Left (forward) facing signal
* { = Right (reverse) facing signal
* TTTTTTT = Train

###Layout
|-X-TTTTTT-X-}-|-{-X-------X-}-|-{-X--------|

Each section has a valid direction which a train can travel, either forward (to the right), reverse (to the left) or bi-directional. This is configured as "F","R" and "B" respectively. Additionally the config must define the connections between the sections, in this case stating that section 2 is forward of section 1, section 1 is reverse of section 2 etc (see config file)

In order to defined the position of signals and sensors in the section forward "F" and reverse "R" locations are also used. The direction a signal faces is assumed from the placement! 

In order to effectively control signals the number of aspects should be defined. A number of assumptions are made at this point:
	2 aspect = Red/Amber
	3 aspect = Red/Amber/Green
	4 aspect = Red/Amber/Green/Amber
	Feathers (direction indicators) not yet supported
If you have a 2 aspect signal of red/other ensure that the other is plugged into the amber output of the control board. 

Lastly we need to define where out train is so we can sense its movement and control it. A train has a DCC id, a number of sensor activators (if using the magnets and hall effect switch approach recommended) and a number of "sections" the train is in. As a train could be present over two sections this parameter is defined as an array of sections ids.

## control.py 

control.py actually reads the config, handles inputs and responds to these in order to control the state of every object in the layout. 

This version (1.0) of control.py is designed to enable semi-automatic control of the layout. This means that everything EXCEPT THE TRAIN can be controlled automatically. Version 1.0 detects the postion, reads the direction and speed of the train but does not control it. 

By responding to sensor events, control.py will automatically change signal colours.

By responding to a change of direction of the train, control.py will attempt to reverse the direction of the sections and signals to keep up with a user moving a train around a layout. 

Since there are no turnouts in the example config, this is a strait forward example thus far.  

## The technical bit

control.py reads and publishes commands from and to a message queue. This way many, many, many components can send control messages. Thus it is also possible to test control.py without a full blown layout full of electronics. 

In order to make control.py work requires a redis message queue server to be running on the same machine as control.py.

Once this is running you can trigger sensor events with the publisher.py script from the redis directory. 

To trigger Sensors and move train from one section to another

> python publisher.py sensors 20,0x08,1

This pushes a simple message to the sensors queue stating that sensor 0x08 on address 20 was activated (1). The addresses and locations of the sensors are specified in the config and consumed by control.py

Likewise to control a train we can publish a change of direction event to the train queue:

> python publisher.py trains 3,Direction,R

### Testing control.py

In order to test control.py we can add the following events to be processed on our message queue:

Activate the first sensor in section 2, meaning train 3 is now in sections 1 and 2. This will change signal 1 to red. 

> python publisher.py sensors 20,0x04,1

Activate this sensor again to represent the back of train 3 entering the section, thus leaving section 1. No change to signals.

> python publisher.py sensors 20,0x04,1

Reverse the direction of the train. This will reverse the signals meaning that all signals go red except signal 2 which goes amber.

> python publisher.py trains 3,Direction,R

Move train 3 back to section 1:

> python publisher.py sensors 20,0x02,1

> python publisher.py sensors 20,0x02,1

Reverse the train to face forward again and we are back to stage one with a green and amber signal in the forward direction.

> python publisher.py trains 3,Direction,F

ENJOY!
