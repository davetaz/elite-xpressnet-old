# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep

r = redis.Redis()
print "Setting direction of T016 to forward"
r.rpush("trains","16,Direction,F")
sleep(5)
print "Activting first sensor in section 2 (33,A,16), first time"
r.rpush("sensors","33,A,16")
sleep(5)
exit(1);
print "Activting first sensor in section 2 (33,A,16), second time"
r.rpush("sensors","33,A,16")
sleep(5)
print "Activting first sensor in section 3 (33,A,32), first time"
r.rpush("sensors","33,A,32")
sleep(5)
print "Activting first sensor in section 3 (33,A,32), second time"
r.rpush("sensors","33,A,32")
sleep(5)
print "activting second sensor in section 3 (32,a,32), first time"
r.rpush("sensors","32,A,32")
sleep(5)
print "Activting first sensor in section 5 (33,A,16), first time"
r.rpush("sensors","32,A,16")
sleep(5)
print "activting second sensor in section 3 (32,A,32), second time"
r.rpush("sensors","32,A,32")
sleep(5)
print "Activting first sensor in section 5 (33,A,16), second time"
r.rpush("sensors","32,A,16")
sleep(5)
print "Activting second sensor in section 5 (32,A,4), first time"
r.rpush("sensors","32,A,4")
sleep(5)
print "Activting first sensor in section 6 (33,A,2), first time"
r.rpush("sensors","32,A,2")
sleep(5)
print "Activting second sensor in section 5 (32,A,4), second time"
r.rpush("sensors","32,A,4")
sleep(5)
print "Activting first sensor in section 6 (33,A,2), second time"
r.rpush("sensors","32,A,2")
sleep(5)
print "Activting second sensor in section 6 (33,A,1), ONLY time"
r.rpush("sensors","32,A,1")
sleep(5)

