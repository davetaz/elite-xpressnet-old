# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep

r = redis.Redis()

print "Activting first sensor in section 2 (32,A,4), first time"
r.rpush("sensors","32,A,4")
sleep(5)
print "Activting first sensor in section 2 (32,A,4), second time"
r.rpush("sensors","32,A,4")
sleep(5)
print "Reverse direction of train to face reverse"
r.rpush("trains","3,Direction,R")
sleep(5)
print "Activting first sensor in section 1 (32,A,2), first time"
r.rpush("sensors","32,A,2")
sleep(5)
print "Activting first sensor in section 1 (32,A,4), second time"
r.rpush("sensors","32,A,2")
sleep(5)
print "Reverse direction of train to face forward again"
r.rpush("trains","3,Direction,F")
