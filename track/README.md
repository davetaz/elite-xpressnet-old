The json file defines 2 strait bits of bi-directional signal track connected to each other, each with 2 sensors and one signal.

Where x is a sensor and T is a signal and >>>> is a train:

   Section #1        Section #2
|--x-->>>>--x-T--|--T-x--------x--|
           FORWARD ----->

To trigger Sensors and move train from one section to another

> python publisher.py sensors 20,0x08,1

This pushes a simple message to the sensors queue stating that sensor 0x08 on address 20 was activated (1). Not sure that de-activation messages will be required. The addresses and locations of the sensors are specified in the config and consumed by control.py
