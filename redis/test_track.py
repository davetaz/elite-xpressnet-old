# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep

r = redis.Redis()

print "Activting first sensor in section 2 (20,A,0x04), first time"
r.rpush("sensors","20,A,0x04,1")
sleep(5)
print "Activting first sensor in section 2 (20,A,0x04), second time"
r.rpush("sensors","20,A,0x04,1")
sleep(5)
print "Reverse direction of train to face reverse"
r.rpush("trains","3,Direction,R")
sleep(5)
print "Activting first sensor in section 1 (20,A,0x02), first time"
r.rpush("sensors","20,A,0x02,1")
sleep(5)
print "Activting first sensor in section 1 (20,A,0x04), second time"
r.rpush("sensors","20,A,0x02,1")
sleep(5)
print "Reverse direction of train to face forward again"
r.rpush("trains","3,Direction,F")
